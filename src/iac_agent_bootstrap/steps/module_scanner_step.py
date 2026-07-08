from pathlib import Path

from iac_agent_bootstrap.scanners.module_scanner import ModuleScanner
from iac_agent_bootstrap.context import BootstrapContext


class ModuleScannerStep:
    def __init__(self) -> None:
        self.scanner = ModuleScanner()

    def run(self, context: BootstrapContext) -> BootstrapContext:
        modules = self.scanner.scan(context.repos_path)

        paths_to_process = {
            str(Path(repo.local_path).as_posix())
            for repo in context.repositories_to_process
            if repo.repository_type == "module"
        }

        if not paths_to_process:
            context.modules_scanned = []
            return context

        context.modules_scanned = [
            module
            for module in modules
            if str(Path(module["path"]).as_posix()) in paths_to_process
        ]

        return context