import typer
from rich.console import Console

from iac_agent_bootstrap.bootstrap_workflow import BootstrapWorkflow
from iac_agent_bootstrap.knowledge.local_knowledge_repository import LocalKnowledgeRepository
from iac_agent_bootstrap.knowledge.module_query_service import ModuleQueryService
from iac_agent_bootstrap.knowledge.spoke_query_service import SpokeQueryService
from iac_agent_bootstrap.knowledge.capability_query_service import CapabilityQueryService
from iac_agent_bootstrap.knowledge.change_decision_service import ChangeDecisionService
from iac_agent_bootstrap.knowledge.reasoning.module_reasoner import ModuleReasoner
from iac_agent_bootstrap.knowledge.reasoning.spoke_reasoner import SpokeReasoner
from iac_agent_bootstrap.knowledge.reasoning.change_reasoner import ChangeReasoner

from iac_agent_bootstrap.knowledge.analysis.requirement_intent import RequirementIntent
from iac_agent_bootstrap.knowledge.analysis.requirement_analysis_service import RequirementAnalysisService
from iac_agent_bootstrap.knowledge.analysis.simple_intent_parser import SimpleIntentParser
from iac_agent_bootstrap.knowledge.analysis.requirement_analysis_facade import (
    RequirementAnalysisFacade,
)


bootstrap_app = typer.Typer()
console = Console()


@bootstrap_app.command()
def bootstrap_aws():
    BootstrapWorkflow().run()

@bootstrap_app.command("knowledge-modules")
def knowledge_modules():
    repo = LocalKnowledgeRepository()
    service = ModuleQueryService(repo)

    console.print(service.list_modules())


@bootstrap_app.command("knowledge-spokes")
def knowledge_spokes():
    repo = LocalKnowledgeRepository()
    service = SpokeQueryService(repo)

    console.print(service.list_spokes())


@bootstrap_app.command("knowledge-capabilities")
def knowledge_capabilities(module_key: str):
    repo = LocalKnowledgeRepository()
    service = CapabilityQueryService(repo)

    console.print(service.list_capabilities(module_key))


@bootstrap_app.command("knowledge-decide")
def knowledge_decide(
    module_key: str,
    capability: str,
):
    repo = LocalKnowledgeRepository()
    module_service = ModuleQueryService(repo)
    capability_service = CapabilityQueryService(repo)

    decision_service = ChangeDecisionService(
        module_query_service=module_service,
        capability_query_service=capability_service,
    )

    console.print(
        decision_service.decide(
            module_key=module_key,
            requested_capability=capability,
        )
    )

@bootstrap_app.command("knowledge-analyze-change")
def knowledge_analyze_change(
    module_key: str,
    capability: str,
):
    repo = LocalKnowledgeRepository()

    module_service = ModuleQueryService(repo)
    capability_service = CapabilityQueryService(repo)
    spoke_service = SpokeQueryService(repo)

    module_reasoner = ModuleReasoner(
        module_query_service=module_service,
        capability_query_service=capability_service,
    )

    spoke_reasoner = SpokeReasoner(
        spoke_query_service=spoke_service,
    )

    change_reasoner = ChangeReasoner(
        module_reasoner=module_reasoner,
        spoke_reasoner=spoke_reasoner,
    )

    console.print(
        change_reasoner.analyze_change(
            module_key=module_key,
            requested_capability=capability,
        )
    )

@bootstrap_app.command("knowledge-analyze-intent")
def knowledge_analyze_intent(
    module_key: str,
    resource_name: str,
    capabilities: str,
    target_spoke: str | None = None,
):
    repo = LocalKnowledgeRepository()
    module_service = ModuleQueryService(repo)
    capability_service = CapabilityQueryService(repo)

    service = RequirementAnalysisService(
        module_query_service=module_service,
        capability_query_service=capability_service,
    )

    intent = RequirementIntent(
        module_key=module_key,
        resource_name=resource_name,
        requested_capabilities=[
            item.strip()
            for item in capabilities.split(",")
            if item.strip()
        ],
        target_spoke=target_spoke,
    )

    console.print(service.analyze(intent))

@bootstrap_app.command("knowledge-analyze-prompt")
def knowledge_analyze_prompt(prompt: str):
    facade = RequirementAnalysisFacade()
    console.print(facade.analyze_prompt(prompt))