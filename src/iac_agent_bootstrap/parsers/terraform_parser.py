import re
from pathlib import Path


class TerraformParser:
    VARIABLE_PATTERN = re.compile(r'variable\s+"([^"]+)"')
    OUTPUT_PATTERN = re.compile(r'output\s+"([^"]+)"')

    def extract_inputs(self, module_path: Path) -> list[str]:
        return self._extract_from_files(
            module_path=module_path,
            pattern=self.VARIABLE_PATTERN,
        )

    def extract_outputs(self, module_path: Path) -> list[str]:
        return self._extract_from_files(
            module_path=module_path,
            pattern=self.OUTPUT_PATTERN,
        )

    def _extract_from_files(self, module_path: Path, pattern: re.Pattern) -> list[str]:
        results = []

        for tf_file in module_path.glob("*.tf"):
            content = tf_file.read_text(encoding="utf-8", errors="ignore")
            results.extend(pattern.findall(content))

        return sorted(set(results))