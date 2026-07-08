import json

import boto3


class S3ArtifactPublisher:
    def __init__(
        self,
        bucket_name: str,
        prefix: str = "knowledge-base",
        region_name: str = "ap-southeast-2",
    ) -> None:
        self.bucket_name = bucket_name
        self.prefix = prefix.strip("/")
        self.client = boto3.client("s3", region_name=region_name)

    def publish(self, artifacts: dict) -> None:
        self._put_json("knowledge_base.json", artifacts["knowledge_base.json"])
        self._put_json("metadata.json", artifacts["metadata.json"])
        self._put_json("repositories.json", artifacts["repositories.json"])
        self._put_json("artifact_index.json", artifacts["artifact_index.json"])

        for filename, payload in artifacts.get("modules", {}).items():
            self._put_json(f"modules/{filename}", payload)

        for filename, payload in artifacts.get("spokes", {}).items():
            self._put_json(f"spokes/{filename}", payload)

    def _put_json(self, relative_key: str, payload: dict) -> None:
        key = f"{self.prefix}/{relative_key}"

        self.client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=json.dumps(payload, indent=2).encode("utf-8"),
            ContentType="application/json",
        )