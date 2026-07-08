from iac_agent_bootstrap.knowledge.knowledge_repository import KnowledgeRepository


class ModuleQueryService:
    def __init__(self, repository: KnowledgeRepository) -> None:
        self.repository = repository

    def list_modules(self) -> list[str]:
        return self.repository.list_modules()

    def get_variables(self, module_key: str) -> dict:
        module = self.repository.get_module(module_key)
        return module.get("schema", {}).get("variables", {})

    def get_outputs(self, module_key: str) -> dict:
        module = self.repository.get_module(module_key)
        return module.get("schema", {}).get("outputs", {})

    def get_resources(self, module_key: str) -> dict:
        module = self.repository.get_module(module_key)
        return module.get("schema", {}).get("resources", {})

    def get_capabilities(self, module_key: str) -> dict:
        module = self.repository.get_module(module_key)
        return module.get("knowledge", {}).get("capabilities", {})

    def exists(self, module_key: str) -> bool:
        return bool(self.repository.get_module(module_key))