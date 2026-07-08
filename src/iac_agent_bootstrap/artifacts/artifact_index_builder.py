from datetime import datetime, timezone


class ArtifactIndexBuilder:
    def build(self, artifacts: dict) -> dict:
        modules = sorted(artifacts.get("modules", {}).keys())
        spokes = sorted(artifacts.get("spokes", {}).keys())

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "artifacts": {
                "knowledge_base": "knowledge_base.json",
                "metadata": "metadata.json",
                "repositories": "repositories.json",
                "modules": [
                    f"modules/{filename}"
                    for filename in modules
                ],
                "spokes": [
                    f"spokes/{filename}"
                    for filename in spokes
                ],
            },
            "counts": {
                "modules": len(modules),
                "spokes": len(spokes),
            },
        }