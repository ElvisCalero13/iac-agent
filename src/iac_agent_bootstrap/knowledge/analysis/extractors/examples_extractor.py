from pathlib import Path


class ExamplesExtractor:
    EXAMPLE_DIRS = [
        "examples",
        "example",
        "usage",
    ]

    def extract(self, module_path: str) -> dict:
        path = Path(module_path)

        return {
            "directories": self._extract_example_dirs(path),
            "readme_terraform_blocks": self._extract_readme_terraform_blocks(path),
        }

    def _extract_example_dirs(self, path: Path) -> dict:
        examples = {}

        for dirname in self.EXAMPLE_DIRS:
            example_dir = path / dirname

            if not example_dir.exists() or not example_dir.is_dir():
                continue

            for tf_file in example_dir.rglob("*.tf"):
                relative_path = str(tf_file.relative_to(path)).replace("\\", "/")

                examples[relative_path] = {
                    "source_file": relative_path,
                    "content": tf_file.read_text(encoding="utf-8"),
                }

        return examples

    def _extract_readme_terraform_blocks(self, path: Path) -> list[dict]:
        readme_path = self._find_readme(path)

        if not readme_path:
            return []

        content = readme_path.read_text(encoding="utf-8")
        blocks = []
        marker = "```"

        parts = content.split(marker)

        for index in range(1, len(parts), 2):
            block = parts[index]

            if block.startswith("hcl") or block.startswith("terraform"):
                lines = block.splitlines()
                language = lines[0].strip() if lines else ""
                body = "\n".join(lines[1:]).strip()

                blocks.append(
                    {
                        "language": language,
                        "content": body,
                    }
                )

        return blocks

    def _find_readme(self, path: Path) -> Path | None:
        for candidate in ["README.md", "readme.md", "README.MD"]:
            readme = path / candidate

            if readme.exists():
                return readme

        return None