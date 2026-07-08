import re
import subprocess
from pathlib import Path


class GitRepositoryInspector:
    def get_remote_url(self, repo_path: Path) -> str:
        raw_url = self._run_git(
            repo_path,
            ["git", "remote", "get-url", "origin"],
        )

        return self.sanitize_url(raw_url)

    def get_current_branch(self, repo_path: Path) -> str:
        branch = self._run_git(
            repo_path,
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        )

        if not branch or branch == "HEAD":
            return "main"

        return branch

    def get_latest_tag(self, repo_path: Path) -> str | None:
        tags = self._run_git(
            repo_path,
            ["git", "tag", "--sort=-v:refname"],
        )

        if not tags:
            return None

        return tags.splitlines()[0]

    def get_repo_name(self, repo_path: Path) -> str:
        remote_url = self.get_remote_url(repo_path)

        if not remote_url:
            return repo_path.name

        return (
            remote_url.rstrip("/")
            .removesuffix(".git")
            .split("/")[-1]
        )

    def sanitize_url(self, repo_url: str) -> str:
        if not repo_url:
            return ""

        return re.sub(
            r"https://[^/@]+:[^/@]+@github\.com/",
            "https://github.com/",
            repo_url,
        )

    def _run_git(
        self,
        cwd: Path,
        command: list[str],
    ) -> str:
        try:
            result = subprocess.run(
                command,
                cwd=str(cwd),
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                return ""

            return result.stdout.strip()

        except Exception:
            return ""