from datetime import datetime, timezone

from iac_agent_bootstrap.checkpoint_store import LocalCheckpointStore
from iac_agent_bootstrap.git_provider import GitProvider
from iac_agent_bootstrap.models import RepositoryCheckpoint
from iac_agent_bootstrap.context import BootstrapContext


class CheckpointUpdateStep:
    def __init__(self) -> None:
        self.store = LocalCheckpointStore()
        self.git = GitProvider()

    def run(self, context: BootstrapContext) -> BootstrapContext:
        indexed_at = datetime.now(timezone.utc).isoformat()

        for repo in context.repositories_to_process:
            checkpoint = RepositoryCheckpoint(
                repo_name=repo.repo_name,
                repository_type=repo.repository_type,
                branch=repo.default_branch,
                last_indexed_commit=self.git.current_commit(repo.local_path),
                last_indexed_tag=self.git.latest_tag(repo.local_path),
                metadata_s3_key=self._metadata_key(repo),
                last_indexed_at=indexed_at,
            )

            self.store.save(checkpoint)

        return context

    def _metadata_key(self, repo) -> str:
        if repo.repository_type == "module":
            return f"knowledge-base/modules/{repo.key}.json"

        return f"knowledge-base/spokes/{repo.key}.json"