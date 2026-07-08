from iac_agent_bootstrap.artifacts.artifact_reader import LocalArtifactReader


class ArtifactQueryService:
    def __init__(self) -> None:
        self.reader = LocalArtifactReader()

    def list_modules(self) -> list[str]:
        index = self.reader.load_index()
        modules = index.get("artifacts", {}).get("modules", [])

        return [
            item.replace("modules/", "").replace(".json", "")
            for item in modules
        ]

    def list_spokes(self) -> list[str]:
        index = self.reader.load_index()
        spokes = index.get("artifacts", {}).get("spokes", [])

        return [
            item.replace("spokes/", "").replace(".json", "")
            for item in spokes
        ]

    def get_module_capabilities(self, module_key: str) -> dict:
        module = self.reader.load_module(module_key)
        return module.get("knowledge", {}).get("capabilities", {})

    def get_module_variables(self, module_key: str) -> dict:
        module = self.reader.load_module(module_key)
        return module.get("schema", {}).get("variables", {})

    def get_module_outputs(self, module_key: str) -> dict:
        module = self.reader.load_module(module_key)
        return module.get("schema", {}).get("outputs", {})

    def get_spoke_modules(self, spoke_key: str) -> dict:
        spoke = self.reader.load_spoke(spoke_key)
        return spoke.get("state", {}).get("modules", {})