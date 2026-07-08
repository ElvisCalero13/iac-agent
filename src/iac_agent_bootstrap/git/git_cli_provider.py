import os
from pathlib import Path

from dotenv import load_dotenv

from iac_agent_bootstrap.git.base_git_provider import BaseGitProvider
from iac_agent_bootstrap.git.git_command_runner import GitCommandRunner


class GitCliProvider(BaseGitProvider):
    def __init__(self) -> None:
        load_dotenv()
        self.git = GitCommandRunner()

    def _with_auth(self, repo_url: str) -> str:
        token = os.getenv("GITHUB_TOKEN")
        username = os.getenv("GITHUB_USERNAME", "x-access-token")

        if not token:
            return repo_url

        if not repo_url.startswith("https://github.com/"):
            return repo_url

        return repo_url.replace(
            "https://github.com/",
            f"https://{username}:{token}@github.com/",
        )
    
    def clone(self, repo_url: str, target_path: Path) -> None:
        auth_url = self._with_auth(repo_url)

        self.git.run(
            ["git", "clone", auth_url, str(target_path)],
            cwd=Path("."),
        )

    def checkout(self, repo_path: Path, ref: str) -> None:
        self.git.run(
            ["git", "checkout", ref],
            cwd=repo_path,
        )

    def create_branch(self, repo_path: Path, branch_name: str) -> None:
        self.git.run(
            ["git", "checkout", "-b", branch_name],
            cwd=repo_path,
        )

    def latest_tag(self, repo_path: Path) -> str | None:
        result = self.git.run(
            ["git", "tag", "--sort=-v:refname"],
            cwd=repo_path,
        )

        tags = [
            line.strip()
            for line in result["stdout"].splitlines()
            if line.strip()
        ]

        return tags[0] if tags else None

    def pull(self, repo_path: Path) -> None:
        self.git.run(
            ["git", "pull"],
            cwd=repo_path,
        )
    
    def has_changes(self, repo_path: Path) -> bool:
        result = self.git.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path,
        )

        return bool(result["stdout"].strip())


    def commit_all(self, repo_path: Path, message: str) -> None:
        self.git.run(
            ["git", "add", "."],
            cwd=repo_path,
        )

        self.git.run(
            ["git", "commit", "-m", message],
            cwd=repo_path,
        )


    def push(self, repo_path: Path, branch_name: str) -> None:
        self.git.run(
            ["git", "push", "-u", "origin", branch_name],
            cwd=repo_path,
        )

    def configure_identity(
        self,
        repo_path: Path,
        user_name: str,
        user_email: str,
    ) -> None:
        self.git.run(
            [
                "git",
                "config",
                "user.name",
                user_name,
            ],
            cwd=repo_path,
        )

        self.git.run(
            [
                "git",
                "config",
                "user.email",
                user_email,
            ],
            cwd=repo_path,
        )
