from iac_agent_bootstrap.knowledge.module_query_service import ModuleQueryService
from iac_agent_bootstrap.knowledge.capability_query_service import CapabilityQueryService


class ModuleReasoner:
    def __init__(
        self,
        module_query_service: ModuleQueryService,
        capability_query_service: CapabilityQueryService,
    ) -> None:
        self.modules = module_query_service
        self.capabilities = capability_query_service

    def analyze_capability(
        self,
        module_key: str,
        capability: str,
    ) -> dict:
        module_exists = self.modules.exists(module_key)

        if not module_exists:
            return {
                "module_key": module_key,
                "capability": capability,
                "module_exists": False,
                "capability_exists": False,
                "requires_module_change": False,
                "reason": "Module does not exist in knowledge base",
            }

        capability_exists = self.capabilities.exists(
            module_key=module_key,
            capability_name=capability,
        )

        return {
            "module_key": module_key,
            "capability": capability,
            "module_exists": True,
            "capability_exists": capability_exists,
            "requires_module_change": not capability_exists,
            "reason": (
                "Capability already exists in module"
                if capability_exists
                else "Capability does not exist in module"
            ),
        }