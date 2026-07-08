from iac_agent_bootstrap.catalog.knowledge_base_catalog import KnowledgeBaseCatalog
from iac_agent_bootstrap.domain.repository_metadata import RepositoryMetadata


class RepositoryCatalog:
    def __init__(
        self,
        catalog_path: str = "data/catalog/knowledge_base.json",
    ) -> None:
        self.knowledge_base = KnowledgeBaseCatalog(catalog_path)

    def get_module_repo(
        self,
        module_name: str,
    ) -> RepositoryMetadata | None:
        repository = self.knowledge_base.get_repository(module_name)

        if not repository:
            return None

        return RepositoryMetadata(
            module_name=repository.get("module_name") or module_name,
            repo_name=repository.get("repo_name") or repository.get("name"),
            repo_url=repository.get("repo_url", ""),
            default_branch=repository.get("default_branch", "main"),
            latest_version=repository.get("latest_version"),
            terraform_source=(
                repository.get("terraform_source")
                or repository.get("repo_url", "")
            ),
        )

    def list_modules(self) -> list[dict]:
        return [
            module.get("repository", {})
            for module in self.knowledge_base.list_modules()
        ]

    def get_spoke(self, spoke_name: str = "caas-spoke") -> dict | None:
        return self.knowledge_base.get_spoke(spoke_name)

    def list_spokes(self) -> list[dict]:
        return self.knowledge_base.list_spokes()