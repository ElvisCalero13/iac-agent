import re
from pathlib import Path

from iac_agent_bootstrap.knowledge.analysis.terraform_block_parser import extract_terraform_block


class ModuleCallsExtractor:
    def extract(self, module_path: str) -> dict:
        path = Path(module_path)
        module_calls = {}

        for tf_file in path.glob("*.tf"):
            content = tf_file.read_text(encoding="utf-8")

            for match in re.finditer(
                r'module\s+"([^"]+)"\s*\{',
                content,
            ):
                name = match.group(1)
                block = extract_terraform_block(content, match.start())

                module_calls[name] = {
                    "name": name,
                    "source_file": tf_file.name,
                    "terraform_block": block,
                    "source": self._extract_source(block),
                }

        return module_calls

    def _extract_source(self, block: str | None) -> str | None:
        if not block:
            return None

        match = re.search(r'source\s*=\s*"([^"]+)"', block)
        return match.group(1) if match else None

