from iac_agent_bootstrap.knowledge.analysis.extractors.variables_extractor import VariablesExtractor
from iac_agent_bootstrap.knowledge.analysis.extractors.outputs_extractor import OutputsExtractor
from iac_agent_bootstrap.knowledge.analysis.extractors.providers_extractor import ProvidersExtractor
from iac_agent_bootstrap.knowledge.analysis.extractors.versions_extractor import VersionsExtractor
from iac_agent_bootstrap.knowledge.analysis.extractors.resources_extractor import ResourcesExtractor
from iac_agent_bootstrap.knowledge.analysis.extractors.data_sources_extractor import DataSourcesExtractor
from iac_agent_bootstrap.knowledge.analysis.extractors.module_calls_extractor import ModuleCallsExtractor
from iac_agent_bootstrap.knowledge.analysis.extractors.locals_extractor import LocalsExtractor
from iac_agent_bootstrap.knowledge.analysis.extractors.readme_extractor import ReadmeExtractor
from iac_agent_bootstrap.knowledge.analysis.extractors.examples_extractor import ExamplesExtractor
from iac_agent_bootstrap.knowledge.analysis.extractors.feature_flags_extractor import FeatureFlagsExtractor
from iac_agent_bootstrap.knowledge.analysis.extractors.capabilities_extractor import CapabilitiesExtractor


class ModuleSchemaExtractor:
    def __init__(self) -> None:
        self.variables_extractor = VariablesExtractor()
        self.outputs_extractor = OutputsExtractor()
        self.providers_extractor = ProvidersExtractor()
        self.versions_extractor = VersionsExtractor()
        self.resources_extractor = ResourcesExtractor()
        self.data_sources_extractor = DataSourcesExtractor()
        self.module_calls_extractor = ModuleCallsExtractor()
        self.locals_extractor = LocalsExtractor()
        self.readme_extractor = ReadmeExtractor()
        self.examples_extractor = ExamplesExtractor()
        self.feature_flags_extractor = FeatureFlagsExtractor()
        self.capabilities_extractor = CapabilitiesExtractor()

    def extract(self, module_path: str) -> dict:
        providers = self.providers_extractor.extract(module_path)
        variables = self.variables_extractor.extract(module_path)
        resources = self.resources_extractor.extract(module_path)
        feature_flags = self.feature_flags_extractor.extract(variables)

        capabilities = self.capabilities_extractor.extract(
            variables=variables,
            resources=resources,
            feature_flags=feature_flags,
        )

        return {
            "variables": variables,
            "outputs": self.outputs_extractor.extract(module_path),
            "providers": providers["provider_blocks"],
            "required_providers": providers["required_providers"],
            "terraform": self.versions_extractor.extract(module_path),
            "resources": resources,
            "data_sources": self.data_sources_extractor.extract(module_path),
            "module_calls": self.module_calls_extractor.extract(module_path),
            "locals": self.locals_extractor.extract(module_path),
            "readme": self.readme_extractor.extract(module_path),
            "examples": self.examples_extractor.extract(module_path),
            "feature_flags": feature_flags,
            "capabilities": capabilities,
        }