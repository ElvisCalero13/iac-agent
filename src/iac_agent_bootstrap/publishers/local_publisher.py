import json
from pathlib import Path


class LocalKnowledgePublisher:
    def __init__(self, output_path: str = "data/catalog/knowledge_base.json") -> None:
        self.output_path = Path(output_path)

    def publish(self, knowledge_base: dict) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        self.output_path.write_text(
            json.dumps(knowledge_base, indent=2),
            encoding="utf-8",
        )