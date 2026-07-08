from pathlib import Path
from abc import ABC, abstractmethod


class BaseGitProvider(ABC):
    @abstractmethod
    def clone(self, repo_url: str, target_path: Path) -> None:
        pass

    @abstractmethod
    def checkout(self, repo_path: Path, ref: str) -> None:
        pass

    @abstractmethod
    def create_branch(self, repo_path: Path, branch_name: str) -> None:
        pass

    @abstractmethod
    def latest_tag(self, repo_path: Path) -> str | None:
        pass

    @abstractmethod
    def pull(self, repo_path: Path) -> None:
        pass
    
    @abstractmethod
    def has_changes(self, repo_path: Path) -> bool:
        pass

    @abstractmethod
    def commit_all(self, repo_path: Path, message: str) -> None:
        pass

    @abstractmethod
    def push(self, repo_path: Path, branch_name: str) -> None:
        pass

    @abstractmethod
    def configure_identity(
        self,
        repo_path: Path,
        user_name: str,
        user_email: str,
    ) -> None:
        pass
