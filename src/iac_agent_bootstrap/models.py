from dataclasses import dataclass
from typing import Literal


RepositoryType = Literal["module", "spoke"]


@dataclass
class RepositoryConfig:
    key: str
    name: str
    repo_name: str
    repo_url: str
    default_branch: str
    base_strategy: str
    local_path: str
    repository_type: RepositoryType


@dataclass
class RepositoryCheckpoint:
    repo_name: str
    repository_type: RepositoryType
    branch: str
    last_indexed_commit: str | None = None
    last_indexed_tag: str | None = None
    metadata_s3_key: str | None = None
    last_indexed_at: str | None = None


@dataclass
class ChangeDecision:
    repo: RepositoryConfig
    should_process: bool
    reason: str
    current_commit: str | None = None
    previous_commit: str | None = None