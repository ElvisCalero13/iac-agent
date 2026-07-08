class ActionBuilder:
    def build(self, analysis: dict) -> list[dict]:
        decision = analysis.get("decision")

        if decision == "module_not_found":
            return [
                {
                    "action": "manual_review",
                    "target": "module_catalog",
                    "reason": "Module not found in knowledge base",
                }
            ]

        if decision == "spoke_only":
            return [
                {
                    "action": "add_module_call",
                    "target": "spoke",
                    "module_key": analysis.get("module_key"),
                    "resource_name": analysis.get("resource_name"),
                },
                {
                    "action": "run_validation",
                    "target": "spoke",
                },
                {
                    "action": "create_pull_request",
                    "target": "spoke",
                },
            ]

        if decision == "module_and_spoke":
            return [
                {
                    "action": "modify_module",
                    "target": "module",
                    "module_key": analysis.get("module_key"),
                    "missing_capabilities": analysis.get("missing_capabilities", []),
                },
                {
                    "action": "run_validation",
                    "target": "module",
                },
                {
                    "action": "create_pull_request",
                    "target": "module",
                },
                {
                    "action": "create_module_tag",
                    "target": "module",
                },
                {
                    "action": "add_module_call",
                    "target": "spoke",
                    "module_key": analysis.get("module_key"),
                    "resource_name": analysis.get("resource_name"),
                },
                {
                    "action": "run_validation",
                    "target": "spoke",
                },
                {
                    "action": "create_pull_request",
                    "target": "spoke",
                },
            ]

        return [
            {
                "action": "manual_review",
                "target": "unknown",
                "reason": "Unknown decision",
            }
        ]