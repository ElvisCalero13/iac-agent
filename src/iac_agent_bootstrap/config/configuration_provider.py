from abc import ABC, abstractmethod

from iac_agent_bootstrap.models import RepositoryConfig


class ConfigurationProvider(ABC):
    @abstractmethod
    def load_seed(self) -> dict:
        pass

    @abstractmethod
    def load_repositories(self) -> list[RepositoryConfig]:
        pass