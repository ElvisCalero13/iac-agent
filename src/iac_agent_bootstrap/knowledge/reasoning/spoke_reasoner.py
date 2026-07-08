from iac_agent_bootstrap.knowledge.spoke_query_service import SpokeQueryService


class SpokeReasoner:
    def __init__(self, spoke_query_service: SpokeQueryService) -> None:
        self.spokes = spoke_query_service

    def find_spokes_using_module(self, module_key: str) -> list[dict]:
        matches = []

        for spoke_key in self.spokes.list_spokes():
            modules = self.spokes.get_modules(spoke_key)

            for block_name, module_data in modules.items():
                source = module_data.get("source") or ""

                if module_key in source:
                    matches.append(
                        {
                            "spoke_key": spoke_key,
                            "block_name": block_name,
                            "source": source,
                            "source_file": module_data.get("source_file"),
                            "inputs": module_data.get("inputs", {}),
                        }
                    )

        return matches