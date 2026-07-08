import re

from iac_agent_bootstrap.knowledge.analysis.requirement_intent import (
    RequirementIntent,
)


class SimpleIntentParser:
    def parse(self, prompt: str) -> RequirementIntent:
        text = prompt.lower()

        module_key = self._detect_module(text)
        resource_name = self._detect_resource_name(text)
        capabilities = self._detect_capabilities(text)

        return RequirementIntent(
            module_key=module_key,
            resource_name=resource_name,
            requested_capabilities=capabilities,
        )

    def _detect_module(self, text: str) -> str:
        if "s3" in text or "bucket" in text:
            return "s3"

        return "unknown"

    def _detect_resource_name(self, text: str) -> str:
        patterns = [
            r"llamado\s+([a-zA-Z0-9_-]+)",
            r"named\s+([a-zA-Z0-9_-]+)",
            r"nombre\s+([a-zA-Z0-9_-]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)

            if match:
                return match.group(1)

        return "default"

    def _detect_capabilities(self, text: str) -> list[str]:
        capabilities = []

        if "kms" in text:
            capabilities.append("kms")

        if "versioning" in text or "versionamiento" in text:
            capabilities.append("versioning")

        if "encryption" in text or "encriptacion" in text or "encriptación" in text:
            capabilities.append("encryption")

        return capabilities