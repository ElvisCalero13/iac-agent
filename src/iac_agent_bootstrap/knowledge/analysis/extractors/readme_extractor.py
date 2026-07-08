from pathlib import Path


class ReadmeExtractor:
    CANDIDATES = [
        "README.md",
        "readme.md",
        "README.MD",
    ]

    def extract(self, module_path: str) -> dict | None:
        path = Path(module_path)

        for candidate in self.CANDIDATES:
            readme_path = path / candidate

            if readme_path.exists():
                return {
                    "source_file": readme_path.name,
                    "content": readme_path.read_text(encoding="utf-8"),
                }

        return None