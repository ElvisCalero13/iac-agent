import json
from pathlib import Path


class LocalKnowledgeLoader:
    def __init__(self, path: str = "data/catalog/knowledge_base.json") -> None:
        self.path = Path(path)

    def load(self) -> dict:
        if not self.path.exists():
            return {
                "metadata": {},
                "repositories": {
                    "modules": {},
                    "spokes": {},
                },
                "spokes_state": {},
                "modules": {},
            }

        return json.loads(
            self.path.read_text(encoding="utf-8")
        )