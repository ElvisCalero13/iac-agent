import os

from iac_agent_bootstrap.artifacts.local_artifact_publisher import LocalArtifactPublisher
from iac_agent_bootstrap.publishers.s3_artifact_publisher import S3ArtifactPublisher


class PublisherFactory:
    @staticmethod
    def create():
        mode = os.getenv("BOOTSTRAP_PUBLISHER", "local")

        if mode == "s3":
            bucket_name = os.environ["BOOTSTRAP_S3_BUCKET"]
            prefix = os.getenv("BOOTSTRAP_S3_PREFIX", "knowledge-base")
            region = os.getenv("AWS_REGION", "ap-southeast-2")

            return S3ArtifactPublisher(
                bucket_name=bucket_name,
                prefix=prefix,
                region_name=region,
            )

        return LocalArtifactPublisher()