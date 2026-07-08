from datetime import datetime, timezone

from iac_agent_bootstrap.context import BootstrapContext
from iac_agent_bootstrap.artifacts.knowledge_artifact_builder import (
    KnowledgeArtifactBuilder,
)
from iac_agent_bootstrap.artifacts.local_artifact_publisher import (
    LocalArtifactPublisher,
)


class KnowledgePublisherStep:
    def __init__(self) -> None:
        self.artifact_builder = KnowledgeArtifactBuilder()
        self.publisher = LocalArtifactPublisher()

    def run(self, context: BootstrapContext) -> BootstrapContext:
        artifacts = self.artifact_builder.build(context.knowledge_base)
        self.publisher.publish(artifacts)

        context.result = {
            "repos_path": context.repos_path,
            "modules_discovered": len(
                context.knowledge_base.get("repositories", {})
                .get("modules", {})
            ),
            "spokes_configured": len(
                context.knowledge_base.get("repositories", {})
                .get("spokes", {})
            ),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "artifacts_generated": {
                "modules": len(artifacts.get("modules", {})),
                "spokes": len(artifacts.get("spokes", {})),
            },
        }

        return context