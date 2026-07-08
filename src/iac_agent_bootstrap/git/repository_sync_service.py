from pathlib import Path

from iac_agent_bootstrap.git.git_cli_provider import GitCliProvider
from iac_agent_bootstrap.models import RepositoryConfig


class RepositorySyncService:
    def __init__(self) -> None:
        self.git = GitCliProvider()

    def sync(
        self,
        repositories: list[RepositoryConfig],
    ) -> dict:
        synced = []

        for repo in repositories:
            result = self._sync_repository(
                repo=repo,
                use_latest_tag=repo.repository_type == "module"
                and repo.base_strategy == "latest_tag",
            )
            synced.append(result)

        return {
            "synced": synced,
            "count": len(synced),
        }

    def _sync_repository(
        self,
        repo: RepositoryConfig,
        use_latest_tag: bool,
    ) -> dict:
        local_path = Path(repo.local_path)

        if not local_path.exists():
            local_path.parent.mkdir(parents=True, exist_ok=True)

            self.git.clone(
                repo_url=repo.repo_url,
                target_path=local_path,
            )
        else:
            self.git.checkout(
                repo_path=local_path,
                ref=repo.default_branch,
            )

            self.git.pull(
                repo_path=local_path,
            )

        checked_out_ref = repo.default_branch

        if use_latest_tag:
            latest_tag = self.git.latest_tag(local_path)

            if latest_tag:
                self.git.checkout(
                    repo_path=local_path,
                    ref=latest_tag,
                )
                checked_out_ref = latest_tag

        return {
            "name": repo.name,
            "repo_name": repo.repo_name,
            "local_path": str(local_path),
            "repository_type": repo.repository_type,
            "checked_out_ref": checked_out_ref,
        }