from iac_agent_bootstrap.change_detector import RepositoryChangeDetector
from iac_agent_bootstrap.context import BootstrapContext


class RepositoryChangeDetectionStep:
    def __init__(self) -> None:
        self.detector = RepositoryChangeDetector()

    def run(self, context: BootstrapContext) -> BootstrapContext:
        for repo in context.repositories_config:
            decision = self.detector.detect(repo)

            context.change_decisions[repo.repo_name] = decision

            if decision.should_process:
                context.repositories_to_process.append(repo)

        return context