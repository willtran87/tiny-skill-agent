"""Optional completion hook over the existing assessment API."""

import asyncio
from collections.abc import Callable, Iterable, Mapping
from typing import Any, Literal

from langchain.agents.middleware import AgentMiddleware, AgentState

from .adapters import inputs_from_messages
from .assessment import AssessmentConfig, AssessmentInputs, AssessmentModel, assess


class AssessmentAgentState(AgentState, total=False):
    """Additive output fields; reserve these names for this middleware."""

    assessment: dict[str, Any] | None
    assessment_error: dict[str, str] | None


class AssessmentMiddleware(AgentMiddleware):
    """Assess on normal agent completion without changing messages or routing.

    Pair with EvidenceMetadataMiddleware for tagged tool messages, or supply an
    input_mapper for explicit records. Default extraction uses all retained
    messages and the supplied static system prompt. Dynamic prompts, history
    scoping, and custom extraction belong in input_mapper.

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
    ):
        if on_error not in {"record", "raise"}:
            raise ValueError("on_error must be 'record' or 'raise'")
        self._model = model
        # AgentMiddleware.tools registers tools: keep this registry separate.
        self._evidence_tools = tuple(tools)
        self._system_prompt = system_prompt
        self._input_mapper = input_mapper
        self._config = AssessmentConfig.model_validate(config or {})
        self._request = request
        self._on_error = on_error

    def before_agent(self, state: AssessmentAgentState, runtime: Any) -> dict[str, Any]:
        # Do not expose a prior turn's successful assessment if this run fails.
        return {"assessment": None, "assessment_error": None}

    async def abefore_agent(self, state: AssessmentAgentState, runtime: Any) -> dict[str, Any]:
        return self.before_agent(state, runtime)

    def after_agent(self, state: AssessmentAgentState, runtime: Any) -> dict[str, Any]:
        try:
            inputs = AssessmentInputs.model_validate(
                self._input_mapper(state) if self._input_mapper is not None
                else inputs_from_messages(
                    state["messages"], self._evidence_tools,
                    system_prompt=self._system_prompt,
                )
            )
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
