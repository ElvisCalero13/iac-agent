import re
from pathlib import Path

from iac_agent_bootstrap.knowledge.analysis.terraform_block_parser import extract_terraform_block


class VersionsExtractor:
    def extract(self, module_path: str) -> dict:
        path = Path(module_path)

        return {
            "terraform_blocks": self._extract_terraform_blocks(path),
            "required_version": self._extract_required_version(path),
        }

    def _extract_terraform_blocks(self, path: Path) -> dict:
        blocks = {}

        for tf_file in path.glob("*.tf"):
            content = tf_file.read_text(encoding="utf-8")

            for match in re.finditer(r'terraform\s*\{', content):
                block = extract_terraform_block(content, match.start())

                if block:
                    blocks[tf_file.name] = {
                        "source_file": tf_file.name,
                        "terraform_block": block,
                    }

        return blocks

    def _extract_required_version(self, path: Path) -> str | None:
        for tf_file in path.glob("*.tf"):
            content = tf_file.read_text(encoding="utf-8")
            match = re.search(
                r'required_version\s*=\s*"([^"]+)"',
                content,
            )

            if match:
                return match.group(1)

        return None

