import re
from pathlib import Path

from iac_agent_bootstrap.knowledge.analysis.terraform_block_parser import extract_terraform_block


class ProvidersExtractor:
    def extract(self, module_path: str) -> dict:
        path = Path(module_path)

        return {
            "provider_blocks": self._extract_provider_blocks(path),
            "required_providers": self._extract_required_providers(path),
        }

    def _extract_provider_blocks(self, path: Path) -> dict:
        providers = {}

        for tf_file in path.glob("*.tf"):
            content = tf_file.read_text(encoding="utf-8")

            for match in re.finditer(r'provider\s+"([^"]+)"\s*\{', content):
                name = match.group(1)
                block = extract_terraform_block(content, match.start())
                alias = self._extract_alias(block) if block else None

                key = f"{name}.{alias}" if alias else name

                providers[key] = {
                    "name": name,
                    "alias": alias,
                    "source_file": tf_file.name,
                    "terraform_block": block,
                }

        return providers

    def _extract_required_providers(self, path: Path) -> dict:
        required = {}

        for tf_file in path.glob("*.tf"):
            content = tf_file.read_text(encoding="utf-8")
            block = self._extract_named_block(
                content=content,
                block_name="required_providers",
            )

            if block:
                required[tf_file.name] = {
                    "source_file": tf_file.name,
                    "terraform_block": block,
                }

        return required

    def _extract_alias(self, block: str | None) -> str | None:
        if not block:
            return None

        match = re.search(r'alias\s*=\s*"([^"]+)"', block)
        return match.group(1) if match else None

    def _extract_named_block(
        self,
        content: str,
        block_name: str,
    ) -> str | None:
        match = re.search(rf'{block_name}\s*\{{', content)

        if not match:
            return None

        return extract_terraform_block(content, match.start())
