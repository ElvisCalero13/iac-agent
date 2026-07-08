from iac_agent_bootstrap.knowledge.reasoning.module_reasoner import ModuleReasoner
from iac_agent_bootstrap.knowledge.reasoning.spoke_reasoner import SpokeReasoner


class ChangeReasoner:
    def __init__(
        self,
        module_reasoner: ModuleReasoner,
        spoke_reasoner: SpokeReasoner,
    ) -> None:
        self.module_reasoner = module_reasoner
        self.spoke_reasoner = spoke_reasoner

    def analyze_change(
        self,
        module_key: str,
        requested_capability: str,
    ) -> dict:
        module_analysis = self.module_reasoner.analyze_capability(
            module_key=module_key,
            capability=requested_capability,
        )

        spokes_using_module = self.spoke_reasoner.find_spokes_using_module(
            module_key=module_key,
        )

        requires_module_change = module_analysis["requires_module_change"]
        requires_spoke_change = module_analysis["module_exists"]

        if not module_analysis["module_exists"]:
            decision = "module_not_found"
        elif requires_module_change:
            decision = "module_and_spoke"
        else:
            decision = "spoke_only"

        return {
            "module_key": module_key,
            "requested_capability": requested_capability,
            "decision": decision,
            "requires_module_change": requires_module_change,
            "requires_spoke_change": requires_spoke_change,
            "module_analysis": module_analysis,
            "spokes_using_module": spokes_using_module,
            "summary": {
                "spokes_impacted": len(spokes_using_module),
            },
        }