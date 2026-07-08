from iac_agent_bootstrap.config.configuration_provider_factory import (
    ConfigurationProviderFactory,
)
from iac_agent_bootstrap.context import BootstrapContext


class RepositoryDiscoveryStep:
    def __init__(self) -> None:
        self.config_provider = ConfigurationProviderFactory.create()

    def run(self, context: BootstrapContext) -> BootstrapContext:
        seed = self.config_provider.load_seed()
        repositories_config = self.config_provider.load_repositories()

        context.seed = seed
        context.repositories_config = repositories_config

        for repo in repositories_config:
            if repo.repository_type == "spoke":
                context.repositories["spokes"][repo.key] = {
                    "name": repo.name,
                    "repo_name": repo.repo_name,
                    "repo_url": repo.repo_url,
                    "default_branch": repo.default_branch,
                    "base_strategy": repo.base_strategy,
                    "local_path": repo.local_path,
                }

        return context