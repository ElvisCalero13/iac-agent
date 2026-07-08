from dataclasses import dataclass, field


@dataclass
class RequirementIntent:
    module_key: str
    resource_name: str
    requested_capabilities: list[str] = field(default_factory=list)
    target_spoke: str | None = None