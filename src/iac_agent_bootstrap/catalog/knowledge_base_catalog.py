import json
from pathlib import Path


class KnowledgeBaseCatalog:
    def __init__(
        self,
        catalog_path: str = "data/catalog/knowledge_base.json",
    ) -> None:
        self.catalog_path = Path(catalog_path)
        self.data = self._load()

    def _load(self) -> dict:
        if not self.catalog_path.exists():
            return {
                "metadata": {},
                "repositories": {"modules": {}, "spokes": {}},
                "modules": {},
            }

        return json.loads(
            self.catalog_path.read_text(encoding="utf-8")
        )

    def get_module(self, module_name: str) -> dict | None:
        modules = self.data.get("modules", {})

        if module_name in modules:
            return modules[module_name]

        for key, module in modules.items():
            metadata = module.get("metadata", {})
            repository = module.get("repository", {})

            if module_name in [
                key,
                metadata.get("name"),
                metadata.get("module_key"),
                repository.get("name"),
                repository.get("repo_name"),
            ]:
                return module

        return None

    def list_modules(self) -> list[dict]:
        return list(self.data.get("modules", {}).values())

    def get_repository(self, module_name: str) -> dict | None:
        module = self.get_module(module_name)

        if not module:
            return None

        return module.get("repository")

    def get_schema(self, module_name: str) -> dict:
        module = self.get_module(module_name)

        if not module:
            return {}

        return module.get("schema", {})

    def get_variable(
        self,
        module_name: str,
        variable_name: str,
    ) -> dict | None:
        return (
            self.get_schema(module_name)
            .get("variables", {})
            .get(variable_name)
        )

    def get_capabilities(self, module_name: str) -> dict:
        module = self.get_module(module_name)

        if not module:
            return {}

        return module.get("knowledge", {}).get("capabilities", {})

    def get_feature_flags(self, module_name: str) -> dict:
        module = self.get_module(module_name)

        if not module:
            return {}

        return module.get("knowledge", {}).get("feature_flags", {})

    def get_spoke(self, spoke_name: str) -> dict | None:
        return (
            self.data
            .get("repositories", {})
            .get("spokes", {})
            .get(spoke_name)
        )

    def list_spokes(self) -> list[dict]:
        return list(
            self.data
            .get("repositories", {})
            .get("spokes", {})
            .values()
        )
    
    def get_spoke_state(self, spoke_name: str) -> dict:
        return (
            self.data
            .get("spokes_state", {})
            .get(spoke_name, {})
        )