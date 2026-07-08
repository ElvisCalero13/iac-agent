from iac_agent_bootstrap.knowledge.knowledge_repository import KnowledgeRepository


class SpokeQueryService:
    def __init__(self, repository: KnowledgeRepository) -> None:
        self.repository = repository

    def list_spokes(self) -> list[str]:
        return self.repository.list_spokes()

    def get_modules(self, spoke_key: str) -> dict:
        spoke = self.repository.get_spoke(spoke_key)
        return spoke.get("state", {}).get("modules", {})

    def get_variables(self, spoke_key: str) -> dict:
        spoke = self.repository.get_spoke(spoke_key)
        return spoke.get("state", {}).get("variables", {})