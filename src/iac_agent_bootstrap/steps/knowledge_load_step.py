from iac_agent_bootstrap.context import BootstrapContext
from iac_agent_bootstrap.knowledge_loader import LocalKnowledgeLoader


class KnowledgeLoadStep:
    def __init__(self) -> None:
        self.loader = LocalKnowledgeLoader()

    def run(self, context: BootstrapContext) -> BootstrapContext:
        context.previous_knowledge_base = self.loader.load()
        return context