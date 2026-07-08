import json
from pathlib import Path

from iac_agent_bootstrap.knowledge.knowledge_repository import KnowledgeRepository


class LocalKnowledgeRepository(KnowledgeRepository):
    def __init__(self, base_path: str = "data/catalog") -> None:
        self.base_path = Path(base_path)

    def list_modules(self) -> list[str]:
        index = self._read_json("artifact_index.json")
        modules = index.get("artifacts", {}).get("modules", [])

        return [
            item.replace("modules/", "").replace(".json", "")
            for item in modules
        ]

    def list_spokes(self) -> list[str]:
        index = self._read_json("artifact_index.json")
        spokes = index.get("artifacts", {}).get("spokes", [])

        return [
            item.replace("spokes/", "").replace(".json", "")
            for item in spokes
        ]

    def get_module(self, module_key: str) -> dict:
        return self._read_json(f"modules/{module_key}.json")

    def get_spoke(self, spoke_key: str) -> dict:
        return self._read_json(f"spokes/{spoke_key}.json")

    def _read_json(self, relative_path: str) -> dict:
        path = self.base_path / relative_path

        if not path.exists():
            return {}

        return json.loads(path.read_text(encoding="utf-8"))