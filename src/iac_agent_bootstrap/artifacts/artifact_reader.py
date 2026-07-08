import json
from pathlib import Path


class LocalArtifactReader:
    def __init__(self, base_path: str = "data/catalog") -> None:
        self.base_path = Path(base_path)

    def load_index(self) -> dict:
        return self._read_json("artifact_index.json")

    def load_metadata(self) -> dict:
        return self._read_json("metadata.json")

    def load_repositories(self) -> dict:
        return self._read_json("repositories.json")

    def load_module(self, module_key: str) -> dict:
        return self._read_json(f"modules/{module_key}.json")

    def load_spoke(self, spoke_key: str) -> dict:
        return self._read_json(f"spokes/{spoke_key}.json")

    def _read_json(self, relative_path: str) -> dict:
        path = self.base_path / relative_path

        if not path.exists():
            return {}

        return json.loads(path.read_text(encoding="utf-8"))