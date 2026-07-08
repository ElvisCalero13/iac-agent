import json
from pathlib import Path


class LocalArtifactPublisher:
    def __init__(self, base_path: str = "data/catalog") -> None:
        self.base_path = Path(base_path)

    def publish(self, artifacts: dict) -> None:
        self.base_path.mkdir(parents=True, exist_ok=True)

        self._write_json(
            self.base_path / "knowledge_base.json",
            artifacts["knowledge_base.json"],
        )

        self._write_json(
            self.base_path / "metadata.json",
            artifacts["metadata.json"],
        )

        self._write_json(
            self.base_path / "repositories.json",
            artifacts["repositories.json"],
        )

        self._write_json(
            self.base_path / "artifact_index.json",
            artifacts["artifact_index.json"],
        )

        modules_path = self.base_path / "modules"
        modules_path.mkdir(parents=True, exist_ok=True)

        for filename, payload in artifacts.get("modules", {}).items():
            self._write_json(modules_path / filename, payload)

        spokes_path = self.base_path / "spokes"
        spokes_path.mkdir(parents=True, exist_ok=True)

        for filename, payload in artifacts.get("spokes", {}).items():
            self._write_json(spokes_path / filename, payload)

    def _write_json(self, path: Path, payload: dict) -> None:
        path.write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )