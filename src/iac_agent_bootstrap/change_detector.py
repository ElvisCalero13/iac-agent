from iac_agent_bootstrap.git_provider import GitProvider
from iac_agent_bootstrap.checkpoint_store import LocalCheckpointStore
from iac_agent_bootstrap.models import ChangeDecision


class RepositoryChangeDetector:
    def __init__(self) -> None:
        self.git = GitProvider()
        self.checkpoints = LocalCheckpointStore()

    def detect(self, repo) -> ChangeDecision:
        current_commit = self.git.current_commit(repo.local_path)
        checkpoint = self.checkpoints.get(repo.repo_name)

        if not checkpoint:
            return ChangeDecision(
                repo=repo,
                should_process=True,
                reason="no_previous_checkpoint",
                current_commit=current_commit,
                previous_commit=None,
            )

        if checkpoint.last_indexed_commit == current_commit:
            return ChangeDecision(
                repo=repo,
                should_process=False,
                reason="repository_unchanged",
                current_commit=current_commit,
                previous_commit=checkpoint.last_indexed_commit,
            )

        return ChangeDecision(
            repo=repo,
            should_process=True,
            reason="commit_changed",
            current_commit=current_commit,
            previous_commit=checkpoint.last_indexed_commit,
        )