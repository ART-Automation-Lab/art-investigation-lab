"""
core/repository/paths.py

Canonical Azure DevOps Feature structure and bug storage path resolution.
Mirrors the Azure DevOps 'ART - Internal Bug Bounty' Epic feature hierarchy.
"""

import os
from typing import List, Dict, Optional, Any


# 1. Canonical list of all 12 Azure DevOps Features under Epic #68782 (ART - Internal Bug Bounty)
CANONICAL_FEATURES: List[str] = [
    "Agent Lab",
    "Orchestrator",
    "Tool Builder",
    "MCP Servers",
    "Triggers",
    "Credential Manager",
    "Serverless Functions",
    "Governance",
    "Human-in-the-Loop / Approvals",
    "Live Connect",
    "ART Deployment Kit (ADK)",
    "Agent X",
]

# 2. Canonical mapping from Feature Name to Filesystem-Safe Feature Directory Name
# Notice: 'Human-in-the-Loop / Approvals' maps to 'Human-in-the-Loop - Approvals' for filesystem safety.
FEATURE_TO_FOLDER_MAP: Dict[str, str] = {
    "Agent Lab": "Agent Lab",
    "Orchestrator": "Orchestrator",
    "Tool Builder": "Tool Builder",
    "MCP Servers": "MCP Servers",
    "Triggers": "Triggers",
    "Credential Manager": "Credential Manager",
    "Serverless Functions": "Serverless Functions",
    "Governance": "Governance",
    "Human-in-the-Loop / Approvals": "Human-in-the-Loop - Approvals",
    "Human-in-the-Loop - Approvals": "Human-in-the-Loop - Approvals",
    "Live Connect": "Live Connect",
    "ART Deployment Kit (ADK)": "ART Deployment Kit (ADK)",
    "ART Development Kit (ADK)": "ART Deployment Kit (ADK)",
    "Agent X": "Agent X",
}

# 3. Canonical directory names of all 12 feature folders
CANONICAL_FEATURE_FOLDERS: List[str] = [
    "Agent Lab",
    "Orchestrator",
    "Tool Builder",
    "MCP Servers",
    "Triggers",
    "Credential Manager",
    "Serverless Functions",
    "Governance",
    "Human-in-the-Loop - Approvals",
    "Live Connect",
    "ART Deployment Kit (ADK)",
    "Agent X",
]

# 4. Supported aliases and module abbreviations (case-insensitive lookup)
FEATURE_ALIASES: Dict[str, str] = {
    # Canonical / module abbreviations
    "AGENT LAB": "Agent Lab",
    "AGENT": "Agent Lab",
    "ORCHESTRATOR": "Orchestrator",
    "ORC": "Orchestrator",
    "TOOL BUILDER": "Tool Builder",
    "TOOL": "Tool Builder",
    "TB": "Tool Builder",
    "TOOLBUILDER": "Tool Builder",
    "MCP SERVERS": "MCP Servers",
    "MCP": "MCP Servers",
    "TRIGGERS": "Triggers",
    "TRIGGER": "Triggers",
    "CREDENTIAL MANAGER": "Credential Manager",
    "CREDENTIALS": "Credential Manager",
    "CREDENTIAL": "Credential Manager",
    "CRED": "Credential Manager",
    "SERVERLESS FUNCTIONS": "Serverless Functions",
    "SERVERLESS": "Serverless Functions",
    "SFN": "Serverless Functions",
    "GOVERNANCE": "Governance",
    "GOV": "Governance",
    "HUMAN-IN-THE-LOOP / APPROVALS": "Human-in-the-Loop / Approvals",
    "HUMAN-IN-THE-LOOP - APPROVALS": "Human-in-the-Loop / Approvals",
    "HUMAN IN THE LOOP": "Human-in-the-Loop / Approvals",
    "HIL": "Human-in-the-Loop / Approvals",
    "LIVE CONNECT": "Live Connect",
    "LIVE": "Live Connect",
    "ART DEPLOYMENT KIT (ADK)": "ART Development Kit (ADK)",
    "ART DEVELOPMENT KIT (ADK)": "ART Development Kit (ADK)",
    "ADK": "ART Development Kit (ADK)",
    "AGENT X": "Agent X",
    "AGENTX": "Agent X",
}


def get_canonical_features() -> List[str]:
    """
    Returns a copy of the canonical Azure DevOps features list.
    Exposed from one location so future ticket-generation and Azure mapping logic can reuse it.
    """
    return list(CANONICAL_FEATURES)


def get_canonical_feature_folders() -> List[str]:
    """
    Returns a copy of the canonical filesystem-safe feature directory names.
    """
    return list(CANONICAL_FEATURE_FOLDERS)


def resolve_feature_folder(feature: str) -> str:
    """
    Resolves a feature name or alias to its canonical filesystem directory name.
    Fails closed: raises ValueError if the feature is unknown or unsupported.
    """
    if not feature or not isinstance(feature, str):
        raise ValueError(f"Feature must be a non-empty string, got: {feature!r}")

    clean = feature.strip()
    if clean in FEATURE_TO_FOLDER_MAP:
        return FEATURE_TO_FOLDER_MAP[clean]

    norm = clean.upper()
    if norm in FEATURE_ALIASES:
        canonical_name = FEATURE_ALIASES[norm]
        return FEATURE_TO_FOLDER_MAP[canonical_name]

    # Check case-insensitive match against canonical features
    for f in CANONICAL_FEATURES:
        if f.upper() == norm:
            return FEATURE_TO_FOLDER_MAP[f]

    raise ValueError(f"Unsupported or unknown feature: '{feature}'")


class BugStoragePath(str):
    """
    A path string representing a resolved bug storage directory.
    Behaves as a string while providing flexible equality checking with or without trailing slash.
    """
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return super().__eq__(other) or self.rstrip("/") == other.rstrip("/")
        return super().__eq__(other)

    def __hash__(self) -> int:
        return hash(self.rstrip("/"))


def resolve_bug_storage_path(
    feature: str,
    bug_id: str,
    base_dir: Optional[str] = None
) -> BugStoragePath:
    """
    Resolves the canonical bug storage path under its Azure DevOps feature folder.
    
    Pattern:
    bugs/<canonical-feature-folder>/<bug_id>/
    
    Or if base_dir is supplied:
    <base_dir>/<canonical-feature-folder>/<bug_id>/
    
    Fails closed (raises ValueError) if feature is unsupported or unknown.
    """
    if not bug_id or not isinstance(bug_id, str):
        raise ValueError(f"bug_id must be a non-empty string, got: {bug_id!r}")

    clean_bug_id = bug_id.strip().strip("/")
    if not clean_bug_id:
        raise ValueError("bug_id cannot be empty or only slashes.")

    folder_name = resolve_feature_folder(feature)

    if base_dir:
        clean_base = base_dir.rstrip("/")
        path = f"{clean_base}/{folder_name}/{clean_bug_id}/"
    else:
        path = f"bugs/{folder_name}/{clean_bug_id}/"

    return BugStoragePath(path)


class FeatureStoragePath(str):
    """
    A path string representing a resolved feature storage directory.
    Behaves as a string while providing flexible equality checking with or without trailing slash.
    """
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return super().__eq__(other) or self.rstrip("/") == other.rstrip("/")
        return super().__eq__(other)

    def __hash__(self) -> int:
        return hash(self.rstrip("/"))


def resolve_feature_storage_path(
    feature: str,
    feature_id: str,
    slug: Optional[str] = None,
    base_dir: Optional[str] = None
) -> FeatureStoragePath:
    """
    Resolves the canonical feature storage path under its Azure DevOps feature folder.
    
    Pattern:
    features/<canonical-feature-folder>/<feature_id>__<slug>/
    or if slug is None:
    features/<canonical-feature-folder>/<feature_id>/
    
    Or if base_dir is supplied:
    <base_dir>/<canonical-feature-folder>/<feature_id>__<slug>/
    
    Fails closed (raises ValueError) if feature is unsupported or unknown.
    """
    if not feature_id or not isinstance(feature_id, str):
        raise ValueError(f"feature_id must be a non-empty string, got: {feature_id!r}")

    clean_feature_id = feature_id.strip().strip("/")
    if not clean_feature_id:
        raise ValueError("feature_id cannot be empty or only slashes.")

    folder_name = resolve_feature_folder(feature)
    dir_name = f"{clean_feature_id}__{slug.strip()}" if slug and slug.strip() else clean_feature_id

    if base_dir:
        clean_base = base_dir.rstrip("/")
        path = f"{clean_base}/{folder_name}/{dir_name}/"
    else:
        path = f"features/{folder_name}/{dir_name}/"

    return FeatureStoragePath(path)
