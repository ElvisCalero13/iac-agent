from pathlib import Path


class SearchTermGenerator:
    def generate(
        self,
        module_name: str,
        module_path: Path,
        category: str,
        inputs: list[str],
        outputs: list[str],
    ) -> list[str]:
        terms = set()

        terms.update(self._split_text(module_name))
        terms.update(self._split_text(str(module_path)))
        terms.update(self._split_text(category))

        for item in inputs:
            terms.update(self._split_text(item))

        for item in outputs:
            terms.update(self._split_text(item))

        return sorted(term for term in terms if term)

    def _split_text(self, value: str) -> list[str]:
        normalized = (
            value.lower()
            .replace("\\", "/")
            .replace("-", " ")
            .replace("_", " ")
            .replace("/", " ")
        )

        return normalized.split()