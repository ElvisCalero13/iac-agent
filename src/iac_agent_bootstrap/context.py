from dataclasses import dataclass, field
from typing import Any

from iac_agent_bootstrap.models import RepositoryConfig


@dataclass
class BootstrapContext:
    repos_path: str
    seed: dict = field(default_factory=dict)
    repositories_config: list[RepositoryConfig] = field(default_factory=list)

    modules_scanned: list[dict] = field(default_factory=list)
    module_schemas: dict[str, dict] = field(default_factory=dict)
    spokes_state: dict[str, dict] = field(default_factory=dict)

    repositories: dict[str, dict] = field(
        default_factory=lambda: {
            "modules": {},
            "spokes": {},
        }
    )

    knowledge_base: dict[str, Any] = field(default_factory=dict)
    result: dict[str, Any] = field(default_factory=dict)

    change_decisions: dict[str, object] = field(default_factory=dict)
    repositories_to_process: list[RepositoryConfig] = field(default_factory=list)
    previous_knowledge_base: dict[str, Any] = field(default_factory=dict)