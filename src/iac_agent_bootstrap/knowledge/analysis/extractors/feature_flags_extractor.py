class FeatureFlagsExtractor:
    PREFIXES = [
        "enable_",
        "is_",
        "use_",
    ]

    def extract(self, variables: dict) -> dict:
        flags = {}

        for name, metadata in variables.items():
            if any(name.startswith(prefix) for prefix in self.PREFIXES):
                flags[name] = metadata

        return flags