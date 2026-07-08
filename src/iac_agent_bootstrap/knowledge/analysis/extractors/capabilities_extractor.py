class CapabilitiesExtractor:
    RULES = {
        "versioning": {
            "keywords": ["versioning", "version"],
        },
        "lifecycle": {
            "keywords": ["lifecycle"],
        },
        "encryption": {
            "keywords": ["sse", "kms", "encryption"],
        },
        "cloudtrail": {
            "keywords": ["cloudtrail"],
        },
        "cloudwatch": {
            "keywords": ["cloudwatch"],
        },
        "replication": {
            "keywords": ["replication"],
        },
        "inventory": {
            "keywords": ["inventory"],
        },
        "notifications": {
            "keywords": ["notification", "notifications"],
        },
    }

    def extract(
        self,
        variables: dict,
        resources: dict,
        feature_flags: dict,
    ) -> dict:
        capabilities = {}

        for capability, rule in self.RULES.items():
            matched_variables = self._match_keys(
                variables,
                rule["keywords"],
            )

            matched_resources = self._match_keys(
                resources,
                rule["keywords"],
            )

            matched_flags = self._match_keys(
                feature_flags,
                rule["keywords"],
            )

            if matched_variables or matched_resources or matched_flags:
                capabilities[capability] = {
                    "variables": matched_variables,
                    "resources": matched_resources,
                    "feature_flags": matched_flags,
                }

        return capabilities

    def _match_keys(
        self,
        items: dict,
        keywords: list[str],
    ) -> list[str]:
        return [
            key
            for key in items.keys()
            if any(keyword in key.lower() for keyword in keywords)
        ]