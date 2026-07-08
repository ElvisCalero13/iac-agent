class DependencyDiscovery:
    def discover(
        self,
        module_name: str,
        category: str,
        inputs: list[str],
        outputs: list[str],
    ) -> list[str]:
        dependencies = set()

        searchable = " ".join(
            [
                module_name,
                category,
                " ".join(inputs),
                " ".join(outputs),
            ]
        ).lower()

        if any(term in searchable for term in ["vpc_id", "subnet_ids", "subnet"]):
            dependencies.add("vpc")

        if any(term in searchable for term in ["target_group", "listener", "alb"]):
            if module_name.lower() != "alb":
                dependencies.add("alb")

        if any(term in searchable for term in ["db_endpoint", "database", "rds"]):
            if module_name.lower() != "rds":
                dependencies.add("rds")

        dependencies.discard(module_name)
        
        return sorted(dependencies)