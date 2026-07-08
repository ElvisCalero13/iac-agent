import re
from pathlib import Path

from iac_agent_bootstrap.knowledge.analysis.terraform_block_parser import extract_terraform_block


class DataSourcesExtractor:
    def extract(self, module_path: str) -> dict:
        path = Path(module_path)
        data_sources = {}

        for tf_file in path.glob("*.tf"):
            content = tf_file.read_text(encoding="utf-8")

            for match in re.finditer(
                r'data\s+"([^"]+)"\s+"([^"]+)"\s*\{',
                content,
            ):
                data_type = match.group(1)
                data_name = match.group(2)
                block = extract_terraform_block(content, match.start())

                key = f"{data_type}.{data_name}"

                data_sources[key] = {
                    "type": data_type,
                    "name": data_name,
                    "source_file": tf_file.name,
                    "terraform_block": block,
                }

        return data_sources

