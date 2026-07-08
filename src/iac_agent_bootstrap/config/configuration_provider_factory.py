import os

from iac_agent_bootstrap.config.configuration_provider import ConfigurationProvider
from iac_agent_bootstrap.config.local_seed_configuration_provider import (
    LocalSeedConfigurationProvider,
)
from iac_agent_bootstrap.config.ssm_configuration_provider import (
    SsmConfigurationProvider,
)


class ConfigurationProviderFactory:
    @staticmethod
    def create() -> ConfigurationProvider:
        mode = os.getenv("BOOTSTRAP_CONFIG_PROVIDER", "local")

        if mode == "ssm":
            parameter_name = os.environ["BOOTSTRAP_CONFIG_PARAMETER"]
            region = os.getenv("AWS_REGION", "ap-southeast-2")

            return SsmConfigurationProvider(
                parameter_name=parameter_name,
                region_name=region,
            )

        return LocalSeedConfigurationProvider()