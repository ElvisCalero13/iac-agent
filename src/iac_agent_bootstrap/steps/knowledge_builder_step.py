import re
from datetime import datetime, timezone
from copy import deepcopy

from iac_agent_bootstrap.context import BootstrapContext


class KnowledgeBuilderStep:
    def run(self, context: BootstrapContext) -> BootstrapContext:
        previous = context.previous_knowledge_base or {}

        knowledge_base = deepcopy(previous) or {
            "metadata": {},
            "repositories": {
                "modules": {},
                "spokes": {},
            },
            "spokes_state": {},
            "modules": {},
        }

        knowledge_base.setdefault("repositories", {})
        knowledge_base["repositories"].setdefault("modules", {})
        knowledge_base["repositories"].setdefault("spokes", {})
        knowledge_base.setdefault("spokes_state", {})
        knowledge_base.setdefault("modules", {})

        # Mantener repositorios configurados desde el seed actual
        knowledge_base["repositories"]["spokes"] = context.repositories["spokes"]

        for module_name, item in context.module_schemas.items():
            module = item["module"]
            module_key = item["module_key"]
            seed_module = item["seed_module"]
            schema = item["schema"]

            repo_url = self._sanitize_repo_url(
                seed_module.get("repo_url")
                or module.get("repo_url")
                or ""
            )

            base_strategy = seed_module.get("base_strategy", "main")

            repository = {
                "module_name": module_key,
                "name": module["name"],
                "repo_name": seed_module.get("repo_name")
                or module.get("repo_name")
                or module["name"],
                "repo_url": repo_url,
                "default_branch": seed_module.get("default_branch")
                or self._normalize_branch(module.get("default_branch")),
                "base_strategy": base_strategy,
                "local_path": seed_module.get("local_path") or module["path"],
            }

            if base_strategy == "latest_tag":
                repository["latest_version"] = (
                    module.get("latest_version") or "v1.1.0"
                )
                repository["terraform_source"] = repo_url

            knowledge_base["repositories"]["modules"][module_key] = repository

            knowledge_base["modules"][module_key] = {
                "repository": repository,
                "metadata": {
                    "name": module["name"],
                    "module_key": module_key,
                    "repo_name": repository["repo_name"],
                    "repo_url": repo_url,
                    "path": module["path"],
                    "category": module.get("category"),
                    "dependencies": module.get("dependencies", []),
                    "base_strategy": base_strategy,
                },
                "schema": {
                    "variables": schema.get("variables", {}),
                    "outputs": schema.get("outputs", {}),
                    "providers": schema.get("providers", {}),
                    "required_providers": schema.get("required_providers", {}),
                    "terraform": schema.get("terraform", {}),
                    "resources": schema.get("resources", {}),
                    "locals": schema.get("locals", {}),
                    "module_calls": schema.get("module_calls", {}),
                    "data_sources": schema.get("data_sources", {}),
                },
                "knowledge": {
                    "features": module.get("features", []),
                    "capabilities": schema.get("capabilities", {}),
                    "feature_flags": schema.get("feature_flags", {}),
                    "examples": schema.get("examples", []),
                    "readme": schema.get("readme"),
                },
                "relationships": {
                    "depends_on": module.get("dependencies", []),
                    "used_by": [],
                },
            }

        for spoke_key, spoke_state in context.spokes_state.items():
            knowledge_base["spokes_state"][spoke_key] = spoke_state

        knowledge_base["metadata"] = {
            "repos_path": context.repos_path,
            "modules_discovered": len(
                knowledge_base["repositories"]["modules"]
            ),
            "spokes_configured": len(
                knowledge_base["repositories"]["spokes"]
            ),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "incremental": True,
            "processed_repositories": [
                repo.repo_name for repo in context.repositories_to_process
            ],
            "skipped_repositories": [
                repo.repo_name
                for repo in context.repositories_config
                if repo not in context.repositories_to_process
            ],
        }

        context.knowledge_base = knowledge_base

        return context

    def _normalize_branch(self, branch: str | None) -> str:
        if not branch or branch == "HEAD":
            return "main"

        return branch

    def _sanitize_repo_url(self, repo_url: str) -> str:
        if not repo_url:
            return ""

        return re.sub(
            r"https://[^/@]+:[^/@]+@github\.com/",
            "https://github.com/",
            repo_url,
        )