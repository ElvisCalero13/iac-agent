from iac_agent.analysis.extractors.spoke_state_extractor import SpokeStateExtractor
from iac_agent_bootstrap.context import BootstrapContext


class SpokeStateStep:
    def __init__(self) -> None:
        self.extractor = SpokeStateExtractor()

    def run(self, context: BootstrapContext) -> BootstrapContext:
        for repo in context.repositories_to_process:
            if repo.repository_type != "spoke":
                continue

            context.spokes_state[repo.key] = self.extractor.extract(
                spoke_path=repo.local_path,
            )

        return context