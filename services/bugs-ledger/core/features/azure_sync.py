"""
core/features/azure_sync.py

Azure Feature Ticket Harness (Harness 02 for Features)
Synchronizes a canonical feature record to Azure DevOps as a User Story
under the 'Backlog Tickets' Epic (#69099) and parent Feature work item.
"""

import os
from typing import Optional, List, Dict, Any, NamedTuple

from core.features.models import FeatureRecord, AzureSyncStatus
from core.features.storage import FeatureStorageManager
from integrations.azure_devops.models import (
    AzureDevOpsConfig,
    AzureWorkItemResult,
    AzureFeatureRouter,
    AzureDevOpsError,
    AZURE_BACKLOG_EPIC_ID,
)
from integrations.azure_devops.client import AzureDevOpsClient


class AzureSyncResult(NamedTuple):
    success: bool
    feature_id: str
    work_item_id: Optional[int]
    work_item_url: Optional[str]
    parent_feature_id: Optional[int]
    is_existing: bool
    sync_status: str
    blocker: Optional[str] = None


class AzureFeatureSyncHarness:
    """
    Authoritative Azure DevOps synchronizer for Feature Requests / Enhancements.
    """

    def __init__(
        self,
        config: Optional[AzureDevOpsConfig] = None,
        client: Optional[AzureDevOpsClient] = None,
        storage_manager: Optional[FeatureStorageManager] = None
    ):
        self.config = config
        self.client = client
        self.storage = storage_manager or FeatureStorageManager()

    def _get_client(self) -> AzureDevOpsClient:
        if self.client:
            return self.client
        if not self.config:
            self.config = AzureDevOpsConfig.from_env()
        self.client = AzureDevOpsClient(self.config)
        return self.client

    def sync_feature(
        self,
        feature_id: str,
        assigned_to: Optional[str] = None,
        dry_run: bool = False
    ) -> AzureSyncResult:
        """
        Executes Azure DevOps synchronization for a canonical feature:
        1. Load record from disk
        2. Preflight validation & module parent resolution
        3. Create or reconcile User Story in Azure DevOps
        4. Readback verification
        5. Write back metadata to disk
        """
        clean_id = feature_id.strip()
        record = self.storage.load_feature(clean_id)
        if not record:
            return AzureSyncResult(
                success=False,
                feature_id=clean_id,
                work_item_id=None,
                work_item_url=None,
                parent_feature_id=None,
                is_existing=False,
                sync_status=AzureSyncStatus.NOT_SYNCED.value,
                blocker=f"Canonical feature record '{clean_id}' not found on disk."
            )

        # Preflight: resolve parent Azure Feature under Backlog Tickets (#69099)
        try:
            parent_feature_id = AzureFeatureRouter.resolve_backlog_feature_id(record.module)
        except AzureDevOpsError as e:
            return AzureSyncResult(
                success=False,
                feature_id=clean_id,
                work_item_id=None,
                work_item_url=None,
                parent_feature_id=None,
                is_existing=False,
                sync_status=AzureSyncStatus.FAILED.value,
                blocker=f"Parent feature resolution failed: {e.message}"
            )

        if dry_run:
            return AzureSyncResult(
                success=True,
                feature_id=clean_id,
                work_item_id=record.azure_work_item_id or 99999,
                work_item_url="https://dev.azure.com/BixBytesSolutions/ART%20IPR-0063/_workitems/edit/dry-run",
                parent_feature_id=parent_feature_id,
                is_existing=bool(record.azure_work_item_id),
                sync_status="DRY_RUN_PASSED"
            )

        # Collect evidence file paths
        feature_dir = self.storage.get_feature_dir(record.module, record.feature_id, record.slug)
        evidence_paths = []
        if os.path.isdir(feature_dir):
            for ef in record.evidence_files:
                fname = ef.get("filename")
                if fname:
                    fpath = os.path.join(feature_dir, fname)
                    if os.path.isfile(fpath):
                        evidence_paths.append(fpath)

        try:
            client = self._get_client()
            ticket_dict = record.to_dict()

            res: AzureWorkItemResult = client.create_user_story(
                feature=ticket_dict,
                canonical_feature_id=record.feature_id,
                parent_work_item_id=parent_feature_id,
                assigned_to=assigned_to,
                evidence_paths=evidence_paths if evidence_paths else None
            )

            # Readback verification
            wi_readback = client.get_work_item(res.work_item_id, expand_relations=True)
            verified_id = int(wi_readback["id"])
            if verified_id != res.work_item_id:
                raise AzureDevOpsError(
                    code="READBACK_VERIFICATION_FAILED",
                    message=f"Work item ID mismatch during readback: expected {res.work_item_id}, got {verified_id}",
                    status_code=502
                )

            # Write back metadata to disk
            record.azure_work_item_id = res.work_item_id
            record.azure_sync_status = AzureSyncStatus.SYNCED.value
            self.storage.save_feature(record)

            return AzureSyncResult(
                success=True,
                feature_id=record.feature_id,
                work_item_id=res.work_item_id,
                work_item_url=res.work_item_url,
                parent_feature_id=parent_feature_id,
                is_existing=res.is_existing,
                sync_status=AzureSyncStatus.SYNCED.value
            )

        except AzureDevOpsError as e:
            record.azure_sync_status = AzureSyncStatus.FAILED.value
            self.storage.save_feature(record)
            return AzureSyncResult(
                success=False,
                feature_id=record.feature_id,
                work_item_id=record.azure_work_item_id,
                work_item_url=None,
                parent_feature_id=parent_feature_id,
                is_existing=False,
                sync_status=AzureSyncStatus.FAILED.value,
                blocker=f"Azure DevOps sync error ({e.code}): {e.message}"
            )
        except Exception as e:
            record.azure_sync_status = AzureSyncStatus.FAILED.value
            self.storage.save_feature(record)
            return AzureSyncResult(
                success=False,
                feature_id=record.feature_id,
                work_item_id=record.azure_work_item_id,
                work_item_url=None,
                parent_feature_id=parent_feature_id,
                is_existing=False,
                sync_status=AzureSyncStatus.FAILED.value,
                blocker=f"Unexpected communication error: {str(e)}"
            )
