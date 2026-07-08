import subprocess
from pathlib import Path


class GitProvider:
    def current_commit(self, repo_path: str) -> str | None:
        path = Path(repo_path)

        if not path.exists():
            return None

        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=path,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return None

        return result.stdout.strip()

    def latest_tag(self, repo_path: str) -> str | None:
        path = Path(repo_path)

        if not path.exists():
            return None

        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=path,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return None

        return result.stdout.strip()