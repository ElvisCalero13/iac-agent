from pathlib import Path

from iac_agent.analysis.module_schema_extractor import ModuleSchemaExtractor
from iac_agent_bootstrap.context import BootstrapContext


class ModuleSchemaStep:
    def __init__(self) -> None:
        self.schema_extractor = ModuleSchemaExtractor()

    def run(self, context: BootstrapContext) -> BootstrapContext:
        seed_modules = context.seed.get("modules", {})
        seed_spokes = context.seed.get("spokes", {})

        spoke_names = {spoke.get("name") for spoke in seed_spokes.values()}
        spoke_repo_names = {spoke.get("repo_name") for spoke in seed_spokes.values()}
        spoke_paths = {
            str(Path(spoke.get("local_path", "")).as_posix())
            for spoke in seed_spokes.values()
        }

        for module in context.modules_scanned:
            module_path = str(Path(module["path"]).as_posix())

            if (
                module["name"] in spoke_names
                or module.get("repo_name") in spoke_repo_names
                or module_path in spoke_paths
            ):
                continue

            module_key = self._module_key(module["name"])
            seed_module = (
                seed_modules.get(module_key)
                or seed_modules.get(module["name"])
                or {}
            )

            schema = self.schema_extractor.extract(
                module_path=module["path"],
            )

            context.module_schemas[module["name"]] = {
                "module": module,
                "module_key": module_key,
                "seed_module": seed_module,
                "schema": schema,
            }

        return context

    def _module_key(self, module_name: str) -> str:
        return module_name.replace("terraform-aws-hub-", "")