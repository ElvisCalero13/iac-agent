from iac_agent_bootstrap.context import BootstrapContext
from iac_agent_bootstrap.steps.repository_discovery_step import RepositoryDiscoveryStep
from iac_agent_bootstrap.steps.repository_sync_step import RepositorySyncStep
from iac_agent_bootstrap.steps.repository_change_detection_step import RepositoryChangeDetectionStep
from iac_agent_bootstrap.steps.knowledge_load_step import KnowledgeLoadStep
from iac_agent_bootstrap.steps.module_scanner_step import ModuleScannerStep
from iac_agent_bootstrap.steps.module_schema_step import ModuleSchemaStep
from iac_agent_bootstrap.steps.spoke_state_step import SpokeStateStep
from iac_agent_bootstrap.steps.knowledge_builder_step import KnowledgeBuilderStep
from iac_agent_bootstrap.steps.knowledge_publisher_step import KnowledgePublisherStep
from iac_agent_bootstrap.steps.checkpoint_update_step import CheckpointUpdateStep


class BootstrapWorkflow:
    def __init__(self) -> None:
        self.steps = [
            RepositoryDiscoveryStep(),
            RepositorySyncStep(),
            RepositoryChangeDetectionStep(),
            KnowledgeLoadStep(),
            ModuleScannerStep(),
            ModuleSchemaStep(),
            SpokeStateStep(),
            KnowledgeBuilderStep(),
            KnowledgePublisherStep(),
            CheckpointUpdateStep(),
        ]

    def run(self, repos_path: str = "data/repositories") -> dict:
        context = BootstrapContext(repos_path=repos_path)

        for step in self.steps:
            context = step.run(context)

        return context.result