import re
from pathlib import Path

from iac_agent_bootstrap.knowledge.analysis.terraform_block_parser import extract_terraform_block


class SpokeStateExtractor:
    def extract(self, spoke_path: str) -> dict:
        path = Path(spoke_path)

        return {
            "modules": self._extract_modules(path),
            "variables": self._extract_variables(path),
        }

    def _extract_modules(self, path: Path) -> dict:
        modules = {}

        for tf_file in path.glob("*.tf"):
            content = tf_file.read_text(encoding="utf-8")

            for match in re.finditer(r'module\s+"([^"]+)"\s*\{', content):
                block_name = match.group(1)
                block = extract_terraform_block(content, match.start())

                modules[block_name] = {
                    "block_name": block_name,
                    "source_file": tf_file.name,
                    "source": self._extract_attribute(block, "source"),
                    "inputs": self._extract_inputs(block),
                    "terraform_block": block,
                }

        return modules

    def _extract_variables(self, path: Path) -> dict:
        variables = {}

        for tf_file in path.glob("*.tf"):
            content = tf_file.read_text(encoding="utf-8")

            for match in re.finditer(r'variable\s+"([^"]+)"\s*\{', content):
                name = match.group(1)
                block = extract_terraform_block(content, match.start())

                variables[name] = {
                    "name": name,
                    "source_file": tf_file.name,
                    "terraform_block": block,
                }

        return variables

    def _extract_inputs(self, block: str | None) -> dict:
        if not block:
            return {}

        inputs = {}

        for line in block.splitlines():
            match = re.match(
                r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+?)\s*$',
                line,
            )

            if not match:
                continue

            key = match.group(1)
            value = match.group(2).strip()

            if key == "source":
                continue

            inputs[key] = value

        return inputs

    def _extract_attribute(
        self,
        block: str | None,
        attribute_name: str,
    ) -> str | None:
        if not block:
            return None

        match = re.search(
            rf'^\s*{re.escape(attribute_name)}\s*=\s*"([^"]+)"',
            block,
            flags=re.MULTILINE,
        )

        return match.group(1) if match else None

