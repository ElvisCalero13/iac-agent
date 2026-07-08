import json
from pathlib import Path

from iac_agent_bootstrap.models import RepositoryConfig


class LocalSeedConfigProvider:
    def __init__(self, seed_path: str = "data/config/repositories.seed.json") -> None:
        self.seed_path = Path(seed_path)

    def load_seed(self) -> dict:
        if not self.seed_path.exists():
            return {"modules": {}, "spokes": {}}

        return json.loads(self.seed_path.read_text(encoding="utf-8"))

    def load_repositories(self) -> list[RepositoryConfig]:
        seed = self.load_seed()
        repositories: list[RepositoryConfig] = []

        for key, repo in seed.get("modules", {}).items():
            repositories.append(
                RepositoryConfig(
                    key=key,
                    name=repo["name"],
                    repo_name=repo["repo_name"],
                    repo_url=repo["repo_url"],
                    default_branch=repo.get("default_branch", "main"),
                    base_strategy=repo.get("base_strategy", "main"),
                    local_path=repo["local_path"],
                    repository_type="module",
                )
            )

        for key, repo in seed.get("spokes", {}).items():
            repositories.append(
                RepositoryConfig(
                    key=key,
                    name=repo["name"],
                    repo_name=repo["repo_name"],
                    repo_url=repo["repo_url"],
                    default_branch=repo.get("default_branch", "main"),
                    base_strategy=repo.get("base_strategy", "main"),
                    local_path=repo["local_path"],
                    repository_type="spoke",
                )
            )

        return repositories