from iac_agent_bootstrap.context import BootstrapContext
from iac_agent_bootstrap.git.repository_sync_service import RepositorySyncService


class RepositorySyncStep:
    def __init__(self) -> None:
        self.service = RepositorySyncService()

    def run(self, context: BootstrapContext) -> BootstrapContext:
        result = self.service.sync(
            repositories=context.repositories_config,
        )

        context.result["repository_sync"] = result

        return context