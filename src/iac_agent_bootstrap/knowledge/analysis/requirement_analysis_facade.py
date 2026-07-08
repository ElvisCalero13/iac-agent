from iac_agent_bootstrap.knowledge.analysis.simple_intent_parser import (
    SimpleIntentParser,
)
from iac_agent_bootstrap.knowledge.analysis.requirement_analysis_service import (
    RequirementAnalysisService,
)
from iac_agent_bootstrap.knowledge.capability_query_service import (
    CapabilityQueryService,
)
from iac_agent_bootstrap.knowledge.local_knowledge_repository import (
    LocalKnowledgeRepository,
)
from iac_agent_bootstrap.knowledge.module_query_service import ModuleQueryService


class RequirementAnalysisFacade:
    def __init__(self) -> None:
        repository = LocalKnowledgeRepository()

        self.parser = SimpleIntentParser()
        self.analysis_service = RequirementAnalysisService(
            module_query_service=ModuleQueryService(repository),
            capability_query_service=CapabilityQueryService(repository),
        )

    def analyze_prompt(self, prompt: str) -> dict:
        intent = self.parser.parse(prompt)
        analysis = self.analysis_service.analyze(intent)

        return {
            "prompt": prompt,
            "intent": intent.__dict__,
            "facts": analysis,
        }