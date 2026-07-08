import re
from pathlib import Path

from iac_agent_bootstrap.knowledge.analysis.terraform_block_parser import extract_terraform_block


class LocalsExtractor:
    def extract(self, module_path: str) -> dict:
        path = Path(module_path)
        locals_blocks = {}

        for tf_file in path.glob("*.tf"):
            content = tf_file.read_text(encoding="utf-8")

            for index, match in enumerate(
                re.finditer(r'locals\s*\{', content),
                start=1,
            ):
                block = extract_terraform_block(content, match.start())

                if block:
                    key = f"{tf_file.stem}_{index}"

                    locals_blocks[key] = {
                        "name": key,
                        "source_file": tf_file.name,
                        "terraform_block": block,
                    }

        return locals_blocks

