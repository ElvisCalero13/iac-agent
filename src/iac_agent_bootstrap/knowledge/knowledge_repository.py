from abc import ABC, abstractmethod


class KnowledgeRepository(ABC):
    @abstractmethod
    def list_modules(self) -> list[str]:
        pass

    @abstractmethod
    def list_spokes(self) -> list[str]:
        pass

    @abstractmethod
    def get_module(self, module_key: str) -> dict:
        pass

    @abstractmethod
    def get_spoke(self, spoke_key: str) -> dict:
        pass