from iac_agent_bootstrap.knowledge.analysis.requirement_intent import (
    RequirementIntent,
)
from iac_agent_bootstrap.knowledge.module_query_service import ModuleQueryService
from iac_agent_bootstrap.knowledge.capability_query_service import (
    CapabilityQueryService,
)


class RequirementAnalysisService:
    def __init__(
        self,
        module_query_service: ModuleQueryService,
        capability_query_service: CapabilityQueryService,
    ) -> None:
        self.modules = module_query_service
        self.capabilities = capability_query_service

    def analyze(self, intent: RequirementIntent) -> dict:
        module_exists = self.modules.exists(intent.module_key)

        capability_results = {}

        if module_exists:
            capability_results = {
                capability: self.capabilities.exists(
                    module_key=intent.module_key,
                    capability_name=capability,
                )
                for capability in intent.requested_capabilities
            }

        missing_capabilities = [
            capability
            for capability, exists in capability_results.items()
            if not exists
        ]

        supported_capabilities = [
            capability
            for capability, exists in capability_results.items()
            if exists
        ]

        return {
            "knowledge_status": self._knowledge_status(
                module_exists=module_exists,
                missing_capabilities=missing_capabilities,
            ),
            "module": {
                "module_key": intent.module_key,
                "exists": module_exists,
            },
            "resource": {
                "name": intent.resource_name,
            },
            "capabilities": {
                "requested": intent.requested_capabilities,
                "supported": supported_capabilities,
                "missing": missing_capabilities,
                "support_matrix": capability_results,
            },
            "impact": {
                "module_change_required": bool(
                    module_exists and missing_capabilities
                ),
                "spoke_change_required": module_exists,
            },
            "target": {
                "spoke": intent.target_spoke,
            },
        }

    def _knowledge_status(
        self,
        module_exists: bool,
        missing_capabilities: list[str],
    ) -> str:
        if not module_exists:
            return "module_not_found"

        if missing_capabilities:
            return "partial_support"

        return "fully_supported"