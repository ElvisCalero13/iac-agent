import json
from pathlib import Path

from iac_agent_bootstrap.models import RepositoryCheckpoint


class LocalCheckpointStore:
    def __init__(self, path: str = "data/catalog/bootstrap_checkpoints.json") -> None:
        self.path = Path(path)

    def get(self, repo_name: str) -> RepositoryCheckpoint | None:
        data = self._load()
        item = data.get(repo_name)

        if not item:
            return None

        return RepositoryCheckpoint(**item)

    def save(self, checkpoint: RepositoryCheckpoint) -> None:
        data = self._load()
        data[checkpoint.repo_name] = checkpoint.__dict__

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    def _load(self) -> dict:
        if not self.path.exists():
            return {}

        return json.loads(self.path.read_text(encoding="utf-8"))