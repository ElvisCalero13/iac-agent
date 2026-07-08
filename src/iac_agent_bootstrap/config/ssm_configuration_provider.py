import json

import boto3

from iac_agent_bootstrap.config.configuration_provider import ConfigurationProvider
from iac_agent_bootstrap.models import RepositoryConfig


class SsmConfigurationProvider(ConfigurationProvider):
    def __init__(
        self,
        parameter_name: str,
        region_name: str = "ap-southeast-2",
    ) -> None:
        self.parameter_name = parameter_name
        self.client = boto3.client("ssm", region_name=region_name)

    def load_seed(self) -> dict:
        response = self.client.get_parameter(
            Name=self.parameter_name,
            WithDecryption=True,
        )

        return json.loads(response["Parameter"]["Value"])

    def load_repositories(self) -> list[RepositoryConfig]:
        seed = self.load_seed()
        repositories: list[RepositoryConfig] = []

        for key, repo in seed.get("modules", {}).items():
            repositories.append(self._build_repo(key, repo, "module"))

        for key, repo in seed.get("spokes", {}).items():
            repositories.append(self._build_repo(key, repo, "spoke"))

        return repositories

    def _build_repo(self, key: str, repo: dict, repository_type: str) -> RepositoryConfig:
        return RepositoryConfig(
            key=key,
            name=repo["name"],
            repo_name=repo["repo_name"],
            repo_url=repo["repo_url"],
            default_branch=repo.get("default_branch", "main"),
            base_strategy=repo.get("base_strategy", "main"),
            local_path=repo["local_path"],
            repository_type=repository_type,
        )