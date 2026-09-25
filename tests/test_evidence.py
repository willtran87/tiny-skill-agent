import unittest
from types import SimpleNamespace

from langchain.tools import tool
from langchain_core.messages import AIMessage, ToolMessage

from tiny_skill_agent.evidence import (
    EvidenceMetadataMiddleware,
    build_criterion_inventory,
    build_source_catalog,
    collect_evidence,
    criterion_coverage,
    derive_criterion_classifications,
    enrich_record_sources,
    expand_assessments_to_records,
    exact_fact_values,
    tag_tool,
    tagged_result,
    validate_record_sources,
    validate_assessment_batch,
    validate_criterion_labels,
)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        @tool(response_format="content_and_artifact")
        def policy(section: str) -> tuple[str, dict]:
            """Return a section of policy instructions."""
            return tagged_result(
                "[strength] Treat reserves above six months as a strength.",
                "directive",
                source=f"skill:{section}",
            )

        @tool(response_format="content_and_artifact")
        def records() -> tuple[str, dict]:
            """Return the recorded application facts."""
            return tagged_result('["Reserves: 8 months"]', "data")

        self.tools = [
            tag_tool(
                policy, "directive", source_kind="skill",
                source_arg="section", source_prefix="skill:",
            ),
            tag_tool(records, "data"),
        ]
        calls = [
            {"name": "policy", "args": {"section": "liquidity"}, "id": "p1"},
            {"name": "records", "args": {}, "id": "r1"},
        ]
        middleware = EvidenceMetadataMiddleware(self.tools)
        self.messages = [AIMessage(content="", tool_calls=calls)]
        for tool_obj, call in zip(self.tools, calls):
            request = SimpleNamespace(tool_call=call)
            self.messages.append(middleware.wrap_tool_call(
                request, lambda _, t=tool_obj, c=call: t.invoke({"type": "tool_call", **c}),
            ))

    def test_collects_any_tagged_tool_and_validates_exact_sources(self):
        ledger = collect_evidence(self.messages, self.tools, system_prompt="Check facts.")
        self.assertEqual(ledger.directive_sources["system_prompt"], ["Check facts."])
        self.assertEqual(ledger.source_kinds["system_prompt"], "system_prompt")
        self.assertEqual(ledger.source_kinds["skill:liquidity"], "skill")
        self.assertEqual(ledger.source_kinds["tool:records#r1"], "tool")
        self.assertEqual(len(ledger.tool_evidence), 2)
        row = {
            "criterion": "[strength] Treat reserves above six months as a strength.",
            "criterion_source": "skill:liquidity",
            "fact": "Reserves: 8 months",
            "fact_source": "tool:records#r1",
            "classification": "strength",
        }
        validate_record_sources([row], ledger)
        validate_criterion_labels([row])
        self.assertEqual(exact_fact_values('{"nested": ["A", {"count": 2}]}'), {"A", "2"})

    def test_rejects_runtime_kind_mismatch(self):
        self.messages[-1].artifact = {"_meta": {"kind": "directive"}}
        with self.assertRaisesRegex(ValueError, "disagrees"):
            collect_evidence(self.messages, self.tools)

    def test_rejects_missing_runtime_kind(self):
        self.messages[-1].artifact = None
        with self.assertRaisesRegex(ValueError, "missing _meta.kind"):
            collect_evidence(self.messages, self.tools)

    def test_rejects_unobserved_fact_and_skill_label_mismatch(self):
        ledger = collect_evidence(self.messages, self.tools)
        row = {
            "criterion": "[strength] Treat reserves above six months as a strength.",
            "criterion_source": "skill:liquidity",
            "fact": "Reserves: 9 months",
            "fact_source": "tool:records#r1",
            "classification": "concern",
        }
        with self.assertRaisesRegex(ValueError, "not an exact tool-returned value"):
            validate_record_sources([row], ledger)
        row["fact"] = "Reserves: 8 months"
        with self.assertRaisesRegex(ValueError, "does not match the criterion"):
            validate_criterion_labels([row])

    def test_rejects_source_spoofing(self):
        self.messages[1].artifact = {
            "_meta": {"kind": "directive", "source_kind": "skill", "source": "skill:other"}
        }
        with self.assertRaisesRegex(ValueError, "source does not match"):
            collect_evidence(self.messages, self.tools)

    def test_validates_criteria_from_system_prompt_skill_and_tool(self):
        @tool
        def guidelines() -> str:
            """Return an approved criterion from a tool."""
            return "[concern] Treat recent missed payments as a concern."

        tag_tool(guidelines, "directive")
        call = {"name": "guidelines", "args": {}, "id": "g1"}
        middleware = EvidenceMetadataMiddleware([guidelines])
        result = middleware.wrap_tool_call(
            SimpleNamespace(tool_call=call),
            lambda _: ToolMessage(content=guidelines.invoke({}), tool_call_id="g1"),
        )
        messages = [
            *self.messages,
            AIMessage(content="", tool_calls=[call]),
            result,
        ]
        system_line = "[strength] Treat verified reserves as a strength."
        ledger = collect_evidence(messages, [*self.tools, guidelines], system_prompt=system_line)
        base_row = {
            "fact": "Reserves: 8 months",
            "fact_source": "tool:records#r1",
            "classification": "strength",
        }
        rows = [
            {**base_row, "criterion": system_line, "criterion_source": "system_prompt"},
            {**base_row, "criterion": "[strength] Treat reserves above six months as a strength.",
             "criterion_source": "skill:liquidity"},
            {**base_row, "criterion": "[concern] Treat recent missed payments as a concern.",
             "criterion_source": "tool:guidelines#g1", "classification": "concern"},
        ]
        self.assertEqual(ledger.source_kinds["tool:guidelines#g1"], "tool")
        validate_record_sources(rows, ledger)
        validate_criterion_labels(rows)
        with self.assertRaisesRegex(ValueError, "source kind is not allowed"):
            validate_record_sources(rows, ledger, allowed_criterion_source_kinds={"skill"})
        with self.assertRaisesRegex(ValueError, "source ID is not allowed"):
            validate_record_sources(rows, ledger, allowed_criterion_source_ids={"skill:liquidity"})
        wrong_source = {**rows[0], "criterion_source": "skill:liquidity"}
        with self.assertRaisesRegex(ValueError, "not an exact source line"):
            validate_record_sources([wrong_source], ledger)

    def test_rejects_runtime_source_kind_mismatch(self):
        self.messages[1].artifact["_meta"]["source_kind"] = "tool"
        with self.assertRaisesRegex(ValueError, "source kind disagrees"):
            collect_evidence(self.messages, self.tools)

    def test_short_source_ids_expand_before_validation(self):
        ledger = collect_evidence(
            self.messages, self.tools, system_prompt="[concern] Flag unverified income."
        )
        catalog = build_source_catalog(ledger)
        by_source = {
            entry["source_id"]: short_id for short_id, entry in catalog.entries.items()
        }
        self.assertEqual(by_source["system_prompt"], "S1")
        self.assertEqual(catalog.entries[by_source["skill:liquidity"]]["label"], "Skill: liquidity")
        self.assertEqual(catalog.entries[by_source["tool:records#r1"]]["label"], "Tool: records (S3)")
        self.assertNotIn("source_id", catalog.as_prompt_data()["S2"])
        draft = {
            "criterion": "[strength] Treat reserves above six months as a strength.",
            "criterion_source_id": by_source["skill:liquidity"],
            "fact": "Reserves: 8 months",
            "fact_source_id": by_source["tool:records#r1"],
            "classification": "strength",
            "reason": "The reported reserves exceed six months.",
        }
        records = enrich_record_sources([draft], catalog)
        self.assertEqual(records[0]["criterion_source"], "skill:liquidity")
        self.assertEqual(records[0]["fact_source"], "tool:records#r1")
        self.assertEqual(records[0]["criterion_source_label"], "Skill: liquidity")
        validate_record_sources(records, ledger)
        classified = derive_criterion_classifications(records)
        self.assertEqual(classified[0]["classification"], "strength")
        validate_criterion_labels(classified)
        with self.assertRaisesRegex(ValueError, "unknown criterion source ID"):
            enrich_record_sources([{**draft, "criterion_source_id": "S999"}], catalog)
        with self.assertRaisesRegex(ValueError, "unknown fact source ID"):
            enrich_record_sources([{
                **draft, "fact_source_id": by_source["skill:liquidity"]
            }], catalog)

    def test_derives_classification_from_verified_criterion(self):
        row = {"criterion": "[concern] Flag recent missed payments.", "fact": "2"}
        self.assertEqual(
            derive_criterion_classifications([row])[0]["classification"], "concern"
        )
        with self.assertRaisesRegex(ValueError, "does not match the criterion"):
            derive_criterion_classifications([{**row, "classification": "strength"}])

    def test_repeated_identical_tool_results_use_one_short_id(self):
        call = {"name": "records", "args": {}, "id": "r2"}
        middleware = EvidenceMetadataMiddleware(self.tools)
        result = middleware.wrap_tool_call(
            SimpleNamespace(tool_call=call),
            lambda _: self.tools[1].invoke({"type": "tool_call", **call}),
        )
        messages = [*self.messages, AIMessage(content="", tool_calls=[call]), result]
        ledger = collect_evidence(messages, self.tools)
        self.assertEqual(len(ledger.fact_sources), 2)
        catalog = build_source_catalog(ledger)
        self.assertEqual(len(catalog.entries), 2)

    def test_middleware_tags_plain_tool_output(self):
        @tool
        def balances() -> str:
            """Return a balance fact."""
            return "Balance: 100"

        tag_tool(balances, "data", dataset="sample")
        middleware = EvidenceMetadataMiddleware([balances])
        request = SimpleNamespace(tool_call={"name": "balances", "args": {}, "id": "b1"})
        response = middleware.wrap_tool_call(
            request,
            lambda _: ToolMessage(content=balances.invoke({}), tool_call_id="b1"),
        )
        self.assertEqual(
            response.artifact["_meta"],
            {"kind": "data", "source_kind": "tool", "dataset": "sample"},
        )
        messages = [
            AIMessage(
                content="",
                tool_calls=[{"name": "balances", "args": {}, "id": "b1"}],
            ),
            response,
        ]
        ledger = collect_evidence(messages, [balances])
        self.assertEqual(ledger.fact_sources["tool:balances#b1"], "Balance: 100")

    def test_criterion_inventory_and_coverage(self):
        ledger = collect_evidence(
            self.messages, self.tools,
            system_prompt="General guidance.\n[concern] Flag unverified income.",
        )
        catalog = build_source_catalog(ledger)
        inventory = build_criterion_inventory(catalog)
        self.assertEqual(list(inventory), ["C1", "C2"])
        self.assertEqual(inventory["C1"]["criterion_source_id"], "S1")
        self.assertEqual(inventory["C2"]["criterion_source_id"], "S2")
        self.assertEqual(
            list(build_criterion_inventory(catalog, allowed_source_kinds={"skill"})),
            ["C1"],
        )
        self.assertEqual(
            build_criterion_inventory(catalog, allowed_source_ids={"system_prompt"})["C1"]["criterion"],
            "[concern] Flag unverified income.",
        )
        batch = validate_assessment_batch([
            {"criterion_id": "C1", "status": "no_match", "findings": []},
        ], inventory)
        report = criterion_coverage(batch, inventory)
        self.assertEqual(report["no_match"], ["C1"])
        self.assertEqual(report["missing"], ["C2"])
        self.assertFalse(report["complete"])
        provisional = criterion_coverage(batch, inventory, confirmed_no_match=set())
        self.assertEqual(provisional["unconfirmed_no_match"], ["C1"])
        batch.update(validate_assessment_batch([
            {"criterion_id": "C2", "status": "uncertain", "findings": []},
        ], ["C2"]))
        self.assertEqual(criterion_coverage(batch, inventory)["uncertain"], ["C2"])
        batch["C2"] = validate_assessment_batch([
            {"criterion_id": "C2", "status": "matched", "findings": [{
                "fact": "Reserves: 8 months", "fact_source_id": "S3",
                "reason": "Eight months of reserves satisfies the six month reserve criterion.",
            }]},
        ], ["C2"])["C2"]
        self.assertTrue(criterion_coverage(batch, inventory)["complete"])
        rows = expand_assessments_to_records(batch, inventory)
        self.assertEqual(len(rows), 1)
        resolved = enrich_record_sources(rows, catalog)
        validate_record_sources(resolved, ledger)

    def test_rejects_malformed_assessment_batches(self):
        good = {"criterion_id": "C1", "status": "no_match", "findings": []}
        for rows, message in [
            ([good, good], "Duplicate"),
            ([{**good, "criterion_id": "C9"}], "Unrequested"),
            ([{**good, "status": "matched"}], "requires a finding"),
            ([{**good, "findings": [{"fact": "x"}]}], "requires empty findings"),
        ]:
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                validate_assessment_batch(rows, ["C1"])


if __name__ == "__main__":
    unittest.main()
