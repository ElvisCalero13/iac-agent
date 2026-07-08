from iac_agent_bootstrap.knowledge.capability_query_service import CapabilityQueryService
from iac_agent_bootstrap.knowledge.module_query_service import ModuleQueryService


class ChangeDecisionService:
    def __init__(
        self,
        module_query_service: ModuleQueryService,
        capability_query_service: CapabilityQueryService,
    ) -> None:
        self.modules = module_query_service
        self.capabilities = capability_query_service

    def decide(
        self,
        module_key: str,
        requested_capability: str,
    ) -> dict:
        if not self.modules.exists(module_key):
            return {
                "module_key": module_key,
                "requested_capability": requested_capability,
                "decision": "module_not_found",
                "requires_module_change": False,
                "requires_spoke_change": False,
                "reason": "Module does not exist in knowledge base",
            }

        capability_exists = self.capabilities.exists(
            module_key=module_key,
            capability_name=requested_capability,
        )

        if capability_exists:
            return {
                "module_key": module_key,
                "requested_capability": requested_capability,
                "decision": "spoke_only",
                "requires_module_change": False,
                "requires_spoke_change": True,
                "reason": "Capability already exists in module",
            }

        return {
            "module_key": module_key,
            "requested_capability": requested_capability,
            "decision": "module_and_spoke",
            "requires_module_change": True,
            "requires_spoke_change": True,
            "reason": "Capability does not exist in module",
        }