import re
from pathlib import Path

from iac_agent_bootstrap.knowledge.analysis.terraform_block_parser import extract_terraform_block


class ResourcesExtractor:
    def extract(self, module_path: str) -> dict:
        path = Path(module_path)
        resources = {}

        for tf_file in path.glob("*.tf"):
            content = tf_file.read_text(encoding="utf-8")

            for match in re.finditer(
                r'resource\s+"([^"]+)"\s+"([^"]+)"\s*\{',
                content,
            ):
                resource_type = match.group(1)
                resource_name = match.group(2)
                block = extract_terraform_block(content, match.start())

                key = f"{resource_type}.{resource_name}"

                resources[key] = {
                    "type": resource_type,
                    "name": resource_name,
                    "source_file": tf_file.name,
                    "terraform_block": block,
                }

        return resources

