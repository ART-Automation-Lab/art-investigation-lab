"""
tests/test_feature_pipeline.py

Comprehensive safety, regression, and unit test suite for the
ART Feature Backlog Pipeline.
Covers all 14 mandatory test requirements from Phase 7.
"""

import os
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from core.features.models import (
    FeatureRecord,
    FeatureClassification,
    FeatureStatus,
    AzureSyncStatus,
)
from core.features.storage import FeatureStorageManager
from core.features.intake import FeatureIntakeHarness
from core.features.azure_sync import AzureFeatureSyncHarness
from core.features.pipeline import FeaturePipeline
from core.identity.generator import generate_feature_id
from integrations.azure_devops.models import (
    AzureDevOpsConfig,
    AzureFeatureRouter,
    AzureDevOpsError,
    AZURE_BACKLOG_EPIC_ID,
    AZURE_BACKLOG_MODULE_FEATURE_MAP,
    AZURE_BUG_BOUNTY_EPIC_ID,
    AZURE_MODULE_FEATURE_MAP,
)
from integrations.azure_devops.client import AzureDevOpsClient


class TestFeaturePipelineSuite(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.validation_root = os.path.join(self.test_dir, "ART-Product-Validation")
        os.makedirs(self.validation_root, exist_ok=True)
        self.storage = FeatureStorageManager(self.validation_root)
        self.intake = FeatureIntakeHarness(self.storage)
        self.mock_config = AzureDevOpsConfig(
            organization="BixBytesSolutions",
            project="ART IPR-0063",
            pat="dummy_pat_12345"
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # 1. New feature creation in local-only mode
    def test_01_new_feature_creation_local_only(self):
        pipeline = FeaturePipeline(
            intake_harness=self.intake,
            storage_manager=self.storage
        )
        raw_input = {
            "title": "Configurable Agent Response Timeout",
            "module": "Agent Lab",
            "problem_opportunity": "Long-running tasks currently time out with a fixed 30s limit.",
            "proposed_behavior": "Allow users to configure timeout up to 300s in Agent Lab settings.",
            "acceptance_criteria": ["Timeout dropdown available in UI", "Custom value persisted"]
        }
        res = pipeline.run(raw_input=raw_input, local_only=True, is_test=True)

        self.assertTrue(res.success)
        self.assertEqual(res.status, "LOCAL_ONLY_COMPLETE")
        self.assertEqual(res.azure_status, "NOT_RUN")
        self.assertTrue(res.feature_id.startswith("TEST-ART-FEAT-AGENT-"))
        self.assertTrue(os.path.isfile(res.local_storage_path))

        # Verify record on disk
        loaded = self.storage.load_feature(res.feature_id)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.title, "Configurable Agent Response Timeout")
        self.assertEqual(loaded.status, FeatureStatus.PROPOSED.value)
        self.assertEqual(loaded.azure_sync_status, AzureSyncStatus.NOT_SYNCED.value)

    # 2. Existing feature update without allocating a new ID
    def test_02_existing_feature_update_preserves_id(self):
        raw_input = {
            "title": "Custom Tool Execution Sandbox",
            "module": "Tool Builder",
            "problem_opportunity": "Tools execute in a shared runtime.",
            "proposed_behavior": "Provide isolated Docker execution.",
        }
        intake_res1 = self.intake.process_intake(raw_input, is_test=True)
        self.assertTrue(intake_res1.success)
        orig_id = intake_res1.feature_id

        # Update the same feature using feature_id
        update_input = {
            "feature_id": orig_id,
            "title": "Custom Tool Execution Sandbox v2",
            "module": "Tool Builder",
            "proposed_behavior": "Provide isolated Docker execution with resource limits.",
            "acceptance_criteria": ["Resource limits configurable"]
        }
        intake_res2 = self.intake.process_intake(update_input, is_test=True)
        self.assertTrue(intake_res2.success)
        self.assertEqual(intake_res2.feature_id, orig_id)
        self.assertTrue(intake_res2.is_existing)

        loaded = self.storage.load_feature(orig_id)
        self.assertEqual(loaded.title, "Custom Tool Execution Sandbox v2")
        self.assertIn("Resource limits configurable", loaded.acceptance_criteria)

    # 3. Duplicate request detection
    def test_03_duplicate_request_detection(self):
        raw_input1 = {
            "title": "Prompt Versioning and Rollback",
            "module": "Agent Lab",
            "problem_opportunity": "Users cannot revert prompt edits.",
            "proposed_behavior": "Maintain historical prompt revisions."
        }
        res1 = self.intake.process_intake(raw_input1, is_test=True)
        self.assertTrue(res1.success)

        # Attempt to file near-identical request without allow_update
        raw_input2 = {
            "title": "Prompt Versioning and Rollback History",
            "module": "Agent Lab",
            "problem_opportunity": "Users cannot revert prompt edits.",
            "proposed_behavior": "Maintain historical prompt revisions."
        }
        res2 = self.intake.process_intake(raw_input2, is_test=True)
        self.assertFalse(res2.success)
        self.assertIn("Potential duplicate feature detected", res2.blocker)
        self.assertEqual(res2.feature_id, res1.feature_id)

        # Retry near-identical request WITH allow_update=True
        raw_input2["allow_update"] = True
        res3 = self.intake.process_intake(raw_input2, is_test=True)
        self.assertTrue(res3.success)
        self.assertEqual(res3.feature_id, res1.feature_id)
        self.assertTrue(res3.is_existing)

    # 4. Feature ID allocation and collision protection
    def test_04_feature_id_allocation_and_collision_protection(self):
        existing = ["TEST-ART-FEAT-AGENT-001", "TEST-ART-FEAT-AGENT-002"]
        next_id = generate_feature_id("AGENT", existing_ids=existing, is_test=True)
        self.assertEqual(next_id, "TEST-ART-FEAT-AGENT-003")

        # Invalid module raises ValueError
        with self.assertRaises(ValueError):
            generate_feature_id("UNKNOWN_MODULE", existing_ids=[], is_test=True)

        # Sequence overflow > 999 raises OverflowError
        with self.assertRaises(OverflowError):
            generate_feature_id("AGENT", existing_ids=["TEST-ART-FEAT-AGENT-999"], is_test=True)

        # Sequence progression
        id_4 = generate_feature_id("AGENT", existing_ids=existing + ["TEST-ART-FEAT-AGENT-003"], is_test=True)
        self.assertEqual(id_4, "TEST-ART-FEAT-AGENT-004")

    # 5. Correct module routing
    def test_05_correct_module_routing(self):
        test_cases = [
            ("Agent Lab", "Agent Lab"),
            ("AGENT", "Agent Lab"),
            ("Orchestrator", "Orchestrator"),
            ("ORC", "Orchestrator"),
            ("TOOL", "Tool Builder"),
            ("MCP", "MCP Servers"),
            ("TRIGGER", "Triggers"),
            ("CREDENTIAL", "Credential Manager"),
            ("SFN", "Serverless Functions"),
            ("GOV", "Governance"),
            ("HIL", "Human-in-the-Loop / Approvals"),
            ("LIVE", "Live Connect"),
            ("ADK", "ART Development Kit (ADK)"),
            ("AGENTX", "Agent X"),
        ]
        for input_mod, expected in test_cases:
            resolved, err = self.intake.resolve_module(input_mod)
            self.assertIsNone(err, f"Failed for {input_mod}")
            self.assertEqual(resolved, expected)

    # 6. Unknown Azure module parent rejection
    def test_06_unknown_azure_module_parent_rejection(self):
        with self.assertRaises(AzureDevOpsError) as ctx:
            AzureFeatureRouter.resolve_backlog_feature_id("NonExistentModule")
        self.assertEqual(ctx.exception.code, "AZURE_PARENT_NOT_CONFIGURED")

        with self.assertRaises(AzureDevOpsError):
            AzureFeatureRouter.resolve_backlog_feature_id(None)

    # 7. Correct User Story work-item type
    def test_07_correct_user_story_work_item_type(self):
        mock_client = MagicMock()
        mock_client.create_user_story.return_value = MagicMock(
            work_item_id=70001,
            work_item_url="https://dev.azure.com/BixBytesSolutions/ART%20IPR-0063/_workitems/edit/70001",
            canonical_bug_id="TEST-ART-FEAT-AGENT-001",
            is_existing=False
        )
        mock_client.get_work_item.return_value = {"id": 70001, "fields": {"System.WorkItemType": "User Story"}}

        sync_harness = AzureFeatureSyncHarness(
            config=self.mock_config,
            client=mock_client,
            storage_manager=self.storage
        )

        record = FeatureRecord(
            feature_id="TEST-ART-FEAT-AGENT-001",
            title="Export Agents to YAML",
            module="Agent Lab",
            problem_opportunity="Lack of export feature.",
            proposed_behavior="Export button generating YAML."
        )
        self.storage.save_feature(record)

        res = sync_harness.sync_feature(record.feature_id)
        self.assertTrue(res.success)
        self.assertEqual(res.work_item_id, 70001)

        # Check that create_user_story was called
        mock_client.create_user_story.assert_called_once()
        call_kwargs = mock_client.create_user_story.call_args[1]
        self.assertEqual(call_kwargs["parent_work_item_id"], 69102)  # Agent Lab under Backlog Tickets

    # 8. Correct parent hierarchy beneath Backlog Tickets
    def test_08_correct_parent_hierarchy_beneath_backlog_tickets(self):
        # Verify all 12 modules map to Backlog Tickets (#69099) Features
        expected_backlog_features = {
            "Agent Lab": 69102,
            "Orchestrator": 69103,
            "Tool Builder": 69104,
            "MCP Servers": 69105,
            "Triggers": 69106,
            "Credential Manager": 69107,
            "Serverless Functions": 69108,
            "Governance": 69109,
            "Human-in-the-Loop / Approvals": 69110,
            "Live Connect": 69111,
            "ART Development Kit (ADK)": 69112,
            "Agent X": 69113,
        }
        for mod, feat_id in expected_backlog_features.items():
            resolved = AzureFeatureRouter.resolve_backlog_feature_id(mod)
            self.assertEqual(resolved, feat_id, f"Mismatch for {mod}")

        self.assertEqual(AZURE_BACKLOG_EPIC_ID, 69099)

    # 9. Existing Azure ticket reconciliation
    def test_09_existing_azure_ticket_reconciliation(self):
        mock_client = MagicMock()
        mock_client.create_user_story.return_value = MagicMock(
            work_item_id=69500,
            work_item_url="https://dev.azure.com/edit/69500",
            canonical_bug_id="TEST-ART-FEAT-GOV-001",
            is_existing=True  # Reconciled existing ticket
        )
        mock_client.get_work_item.return_value = {"id": 69500}

        sync_harness = AzureFeatureSyncHarness(
            config=self.mock_config,
            client=mock_client,
            storage_manager=self.storage
        )

        record = FeatureRecord(
            feature_id="TEST-ART-FEAT-GOV-001",
            title="Custom Compliance Report Template",
            module="Governance",
            problem_opportunity="Reports use standard format only.",
            proposed_behavior="Allow custom header and metrics."
        )
        self.storage.save_feature(record)

        res = sync_harness.sync_feature(record.feature_id)
        self.assertTrue(res.success)
        self.assertTrue(res.is_existing)
        self.assertEqual(res.work_item_id, 69500)

    # 10. Safe retry following Azure failure
    def test_10_safe_retry_following_azure_failure(self):
        mock_client = MagicMock()
        mock_client.create_user_story.side_effect = AzureDevOpsError(
            code="EXTERNAL_SERVICE_ERROR",
            message="Simulated Azure 502 Bad Gateway",
            status_code=502
        )

        sync_harness = AzureFeatureSyncHarness(
            config=self.mock_config,
            client=mock_client,
            storage_manager=self.storage
        )

        record = FeatureRecord(
            feature_id="TEST-ART-FEAT-ORC-001",
            title="Parallel Branching in Orchestrator",
            module="Orchestrator",
            problem_opportunity="Sequential only.",
            proposed_behavior="Fork-join nodes."
        )
        self.storage.save_feature(record)

        res = sync_harness.sync_feature(record.feature_id)
        self.assertFalse(res.success)
        self.assertIn("Simulated Azure 502", res.blocker)

        # Verify local record is still intact
        reloaded = self.storage.load_feature(record.feature_id)
        self.assertIsNotNone(reloaded)
        self.assertEqual(reloaded.azure_sync_status, AzureSyncStatus.FAILED.value)

        # Retry succeeds
        mock_client.create_user_story.side_effect = None
        mock_client.create_user_story.return_value = MagicMock(
            work_item_id=70100,
            work_item_url="https://dev.azure.com/edit/70100",
            canonical_bug_id="TEST-ART-FEAT-ORC-001",
            is_existing=False
        )
        mock_client.get_work_item.return_value = {"id": 70100}

        retry_res = sync_harness.sync_feature(record.feature_id)
        self.assertTrue(retry_res.success)
        self.assertEqual(retry_res.work_item_id, 70100)

    # 11. Preservation of evidence
    def test_11_preservation_of_evidence(self):
        ev_file = os.path.join(self.test_dir, "mockup_schema.png")
        with open(ev_file, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDRtest_data")

        raw_input = {
            "title": "Visual Schema Node Preview",
            "module": "Agent Lab",
            "problem_opportunity": "No preview of output nodes.",
            "proposed_behavior": "Hover preview of node JSON schema."
        }
        res = self.intake.process_intake(raw_input, evidence_files=[ev_file], is_test=True)
        self.assertTrue(res.success)

        loaded = self.storage.load_feature(res.feature_id)
        self.assertEqual(len(loaded.evidence_files), 1)
        self.assertEqual(loaded.evidence_files[0]["filename"], "mockup_schema.png")
        self.assertTrue(len(loaded.evidence_files[0]["sha256"]) == 64)

        feature_dir = self.storage.get_feature_dir(loaded.module, loaded.feature_id, loaded.slug)
        saved_ev = os.path.join(feature_dir, "mockup_schema.png")
        self.assertTrue(os.path.isfile(saved_ev))

    # 12. Feature ledger consistency
    def test_12_feature_ledger_consistency(self):
        for i in range(1, 4):
            record = FeatureRecord(
                feature_id=f"TEST-ART-FEAT-MCP-00{i}",
                title=f"MCP Server Discovery Protocol v{i}",
                module="MCP Servers",
                classification=FeatureClassification.NEW_FEATURE.value,
                status=FeatureStatus.PROPOSED.value
            )
            self.storage.save_feature(record)

        self.storage.compile_ledger()
        self.assertTrue(os.path.isfile(self.storage.ledger_path))

        with open(self.storage.ledger_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("- **Total Features:** 3", content)
        self.assertIn("- **Proposed:** 3", content)
        self.assertIn("TEST-ART-FEAT-MCP-001", content)
        self.assertIn("TEST-ART-FEAT-MCP-002", content)
        self.assertIn("TEST-ART-FEAT-MCP-003", content)
        self.assertIn("features/MCP%20Servers/", content)

    # 13. Prevention of accidental writes to Epic #68782
    def test_13_prevention_of_accidental_writes_to_bug_epic(self):
        # Backlog features must NEVER resolve to bug bounty parent feature IDs
        for mod, backlog_id in AZURE_BACKLOG_MODULE_FEATURE_MAP.items():
            bug_id = AZURE_MODULE_FEATURE_MAP[mod]
            self.assertNotEqual(
                backlog_id,
                bug_id,
                f"Backlog feature ID matches Bug bounty feature ID for {mod}"
            )
            resolved_backlog = AzureFeatureRouter.resolve_backlog_feature_id(mod)
            self.assertEqual(resolved_backlog, backlog_id)
            self.assertNotEqual(resolved_backlog, bug_id)

    # 14. Patch builder structure for User Story
    def test_14_user_story_patch_builder(self):
        client = AzureDevOpsClient(self.mock_config)
        feature_data = {
            "title": "Import JSON Schema Directly",
            "module": "Agent Lab",
            "classification": "NEW_FEATURE",
            "problem_opportunity": "Manual schema construction is tedious.",
            "proposed_behavior": "Add direct import dialog.",
            "business_impact": "Saves 15 mins per agent.",
            "user_experience": "Clean modal with paste box.",
            "acceptance_criteria": ["Import validates JSON", "Generates correct nodes"],
            "related_bugs": ["ART-AGENT-007", "#68933"],
            "priority": 1
        }
        patch = client._map_feature_to_patch(
            feature=feature_data,
            canonical_feature_id="ART-FEAT-AGENT-001",
            parent_work_item_id=69102
        )

        paths = {p["path"]: p["value"] for p in patch}
        self.assertEqual(paths["/fields/System.Title"], "[ART-FEAT-AGENT-001] Import JSON Schema Directly")
        self.assertEqual(paths["/fields/Microsoft.VSTS.Common.Priority"], 1)
        self.assertEqual(paths["/fields/Microsoft.VSTS.Common.ValueArea"], "Business")
        self.assertIn("ART:ART-FEAT-AGENT-001", paths["/fields/System.Tags"])
        self.assertIn("Import validates JSON", paths["/fields/Microsoft.VSTS.Common.AcceptanceCriteria"])
        self.assertIn("ART-AGENT-007", paths["/fields/System.Description"])

        # Verify parent relation
        relations = [p for p in patch if p["path"] == "/relations/-"]
        self.assertEqual(len(relations), 1)
        self.assertEqual(relations[0]["value"]["rel"], "System.LinkTypes.Hierarchy-Reverse")
        self.assertIn("/workItems/69102", relations[0]["value"]["url"])


if __name__ == "__main__":
    unittest.main()
