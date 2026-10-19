"""Optional completion hook over the existing assessment API."""

import asyncio
from collections.abc import Callable, Iterable, Mapping
from typing import Any, Literal

from langchain.agents.middleware import AgentMiddleware, AgentState
from pydantic import Field, model_validator

from .adapters import inputs_from_messages
from .assessment import AssessmentConfig, AssessmentInputs, AssessmentModel, Record, assess
from .criteria import CriterionExtractor


class AssessmentScope(Record):
    """Application-owned expected source IDs, supplied afresh per invocation."""

    case_id: str = Field(min_length=1)
    source_ids: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def valid_sources(self):
        if not self.case_id.strip() or any(not value.strip() for value in self.source_ids):
            raise ValueError("Case and source IDs must not be blank")
        if len(self.source_ids) != len(set(self.source_ids)):
            raise ValueError("Case scope source IDs must be unique")
        return self


class AssessmentAgentState(AgentState, total=False):
    """Additive output fields; reserve these names for this middleware."""

    assessment: dict[str, Any] | None
    assessment_error: dict[str, str] | None


class AssessmentMiddleware(AgentMiddleware):
    """Assess on normal agent completion without changing messages or routing.

    Pair with EvidenceMetadataMiddleware for tagged tool messages, or supply an
    input_mapper for explicit records. Default extraction uses all retained
    messages and the supplied static system prompt. Opt into scope_from_context
    for explicit case isolation, or use input_mapper for custom extraction.
    criterion_extractor optionally handles prose rules with explicit labels.

    The synchronous assessment callable also runs for ainvoke, in a worker
    thread. Completion waits for assessment; cancellation cannot stop an
    already-running synchronous provider call. Checkpoint replay may repeat
    assessment calls. No exactly-once or background-job guarantee is implied.
    """

    state_schema = AssessmentAgentState

    def __init__(
        self,
        model: AssessmentModel,
        *,
        tools: Iterable[Any] = (),
        system_prompt: str | None = None,
        input_mapper: Callable[[Mapping[str, Any]], AssessmentInputs | Mapping[str, Any]] | None = None,
        config: AssessmentConfig | Mapping[str, Any] | None = None,
        request: str = "",
        on_error: Literal["record", "raise"] = "record",
        scope_from_context: Callable[[Any], AssessmentScope | Mapping[str, Any]] | None = None,
        criterion_extractor: CriterionExtractor | None = None,
    ):
        if on_error not in {"record", "raise"}:
            raise ValueError("on_error must be 'record' or 'raise'")
        if input_mapper is not None and criterion_extractor is not None:
            raise ValueError("A custom input_mapper must configure criterion extraction itself")
        self._model = model
        # AgentMiddleware.tools registers tools: keep this registry separate.
        self._evidence_tools = tuple(tools)
        self._system_prompt = system_prompt
        self._input_mapper = input_mapper
        self._config = AssessmentConfig.model_validate(config or {})
        self._request = request
        self._on_error = on_error
        self._scope_from_context = scope_from_context
        self._criterion_extractor = criterion_extractor

    def before_agent(self, state: AssessmentAgentState, runtime: Any) -> dict[str, Any]:
        # Do not expose a prior turn's successful assessment if this run fails.
        return {"assessment": None, "assessment_error": None}

    async def abefore_agent(self, state: AssessmentAgentState, runtime: Any) -> dict[str, Any]:
        return self.before_agent(state, runtime)

    def after_agent(self, state: AssessmentAgentState, runtime: Any) -> dict[str, Any]:
        try:
            # Runtime context is per invocation, unlike checkpointed state.
            scope = None if self._scope_from_context is None else AssessmentScope.model_validate(
                self._scope_from_context(runtime.context)
            )
            inputs = AssessmentInputs.model_validate(
                self._input_mapper(state) if self._input_mapper is not None
                else inputs_from_messages(
                    state["messages"], self._evidence_tools,
                    system_prompt=self._system_prompt,
                    source_scope_ids=None if scope is None else scope.source_ids,
                    criterion_extractor=self._criterion_extractor,
                )
            )
            if scope is not None:
                used = {r.source_id for r in [*inputs.criteria, *inputs.evidence]}
                if foreign := used - set(scope.source_ids):
                    raise ValueError(f"Assessment inputs escape case {scope.case_id}: {sorted(foreign)}")
                if self._input_mapper is not None and (missing := set(scope.source_ids) - used):
                    raise ValueError(f"Custom assessment inputs omit expected sources: {sorted(missing)}")
            result = assess(
                criteria=inputs.criteria, evidence=inputs.evidence,
                model=self._model, config=self._config, request=self._request,
            )
            return {"assessment": result.model_dump(mode="json"), "assessment_error": None}
        except Exception as exc:
            if self._on_error == "raise":
                raise
            return {"assessment": None, "assessment_error": {
                "type": type(exc).__name__, "message": str(exc),
            }}

    async def aafter_agent(self, state: AssessmentAgentState, runtime: Any) -> dict[str, Any]:
        return await asyncio.to_thread(self.after_agent, state, runtime)
