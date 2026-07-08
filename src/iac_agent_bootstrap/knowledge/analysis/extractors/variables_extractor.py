import re
from pathlib import Path

from iac_agent_bootstrap.knowledge.analysis.terraform_block_parser import extract_terraform_block


class VariablesExtractor:
    def extract(self, module_path: str) -> dict:
        path = Path(module_path)
        variables = {}

        for tf_file in path.glob("*.tf"):
            content = tf_file.read_text(encoding="utf-8")

            for match in re.finditer(r'variable\s+"([^"]+)"\s*\{', content):
                name = match.group(1)
                block = extract_terraform_block(content, match.start())

                if block:
                    variables[name] = {
                        "name": name,
                        "source_file": tf_file.name,
                        "terraform_block": block,
                    }

        return variables

