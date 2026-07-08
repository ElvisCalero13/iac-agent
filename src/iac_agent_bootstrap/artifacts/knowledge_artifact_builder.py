from copy import deepcopy
from iac_agent_bootstrap.artifacts.artifact_index_builder import ArtifactIndexBuilder


class KnowledgeArtifactBuilder:
    def __init__(self) -> None:
        self.index_builder = ArtifactIndexBuilder()

    def build(self, knowledge_base: dict) -> dict:
        metadata = deepcopy(knowledge_base.get("metadata", {}))
        repositories = deepcopy(knowledge_base.get("repositories", {}))
        modules = deepcopy(knowledge_base.get("modules", {}))
        spokes_state = deepcopy(knowledge_base.get("spokes_state", {}))

        artifacts = {
            "knowledge_base.json": knowledge_base,
            "metadata.json": metadata,
            "repositories.json": repositories,
            "modules": {},
            "spokes": {},
        }

        for module_key, module_data in modules.items():
            artifacts["modules"][f"{module_key}.json"] = {
                "module_key": module_key,
                **module_data,
            }

        for spoke_key, spoke_repo in repositories.get("spokes", {}).items():
            artifacts["spokes"][f"{spoke_key}.json"] = {
                "spoke_key": spoke_key,
                "repository": spoke_repo,
                "state": spokes_state.get(spoke_key, {}),
            }

        artifacts["artifact_index.json"] = self.index_builder.build(artifacts)

        return artifacts