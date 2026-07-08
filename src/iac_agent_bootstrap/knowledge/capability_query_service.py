from iac_agent_bootstrap.knowledge.knowledge_repository import KnowledgeRepository


class CapabilityQueryService:
    def __init__(self, repository: KnowledgeRepository) -> None:
        self.repository = repository

    def list_capabilities(self, module_key: str) -> dict:
        module = self.repository.get_module(module_key)
        return module.get("knowledge", {}).get("capabilities", {})

    def exists(
        self,
        module_key: str,
        capability_name: str,
    ) -> bool:
        capabilities = self.list_capabilities(module_key)

        normalized_capability = self._normalize(capability_name)

        for key, value in capabilities.items():
            if self._normalize(key) == normalized_capability:
                return bool(value)

        return False

    def explain(
        self,
        module_key: str,
        capability_name: str,
    ) -> dict:
        exists = self.exists(
            module_key=module_key,
            capability_name=capability_name,
        )

        return {
            "module_key": module_key,
            "capability": capability_name,
            "exists": exists,
            "decision": "spoke_only" if exists else "module_and_spoke",
            "reason": (
                "Capability already exists in module"
                if exists
                else "Capability does not exist in module"
            ),
        }

    def _normalize(self, value: str) -> str:
        return (
            value.lower()
            .replace("-", "_")
            .replace(" ", "_")
            .strip()
        )