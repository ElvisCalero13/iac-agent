import subprocess
from pathlib import Path

from iac_agent_bootstrap.parsers.terraform_parser import TerraformParser
from iac_agent_bootstrap.parsers.search_term_generator import SearchTermGenerator
from iac_agent_bootstrap.discovery.dependency_discovery import DependencyDiscovery
from iac_agent_bootstrap.git.git_repository_inspector import GitRepositoryInspector


class ModuleScanner:
    def __init__(self):
        self.parser = TerraformParser()
        self.search_term_generator = SearchTermGenerator()
        self.dependency_discovery = DependencyDiscovery()
        self.git_inspector = GitRepositoryInspector()

    def scan(self, repos_path: str) -> list[dict]:
        base_path = Path(repos_path)

        if not base_path.exists():
            raise ValueError(f"Repos path does not exist: {repos_path}")

        modules = []

        for module_path in base_path.rglob("*"):
            if not module_path.is_dir():
                continue

            has_tf_files = list(module_path.glob("*.tf"))

            if not has_tf_files:
                continue
            
            category = self._detect_category(module_path)
            inputs = self.parser.extract_inputs(module_path)
            outputs = self.parser.extract_outputs(module_path)
            dependencies = self.dependency_discovery.discover(
                module_name=module_path.name,
                category=category,
                inputs=inputs,
                outputs=outputs,
            )
            search_terms = self.search_term_generator.generate(
                module_name=module_path.name,
                module_path=module_path,
                category=category,
                inputs=inputs,
                outputs=outputs,
            )

            modules.append(
                {
                    "name": module_path.name,
                    "path": str(module_path),
                    "category": category,
                    "tf_files": [file.name for file in has_tf_files],
                    "inputs": inputs,
                    "outputs": outputs,
                    "dependencies": dependencies,
                    "search_terms": search_terms,
                    "repo_name": self.git_inspector.get_repo_name(module_path),
                    "repo_url": self.git_inspector.get_remote_url(module_path),
                    "default_branch": self.git_inspector.get_current_branch(module_path),
                    "latest_version": self.git_inspector.get_latest_tag(module_path),
                }
            )

        return modules
    
    def _detect_category(self, module_path: Path) -> str:
        path = str(module_path).lower()

        if "compute" in path:
            return "compute"

        if "database" in path:
            return "database"

        if "network" in path:
            return "networking"

        if "observability" in path or "monitoring" in path:
            return "observability"

        return "unknown"
    
