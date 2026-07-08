from pydantic import BaseModel


class RepositoryMetadata(BaseModel):
    module_name: str
    repo_name: str
    repo_url: str
    default_branch: str = "main"
    latest_version: str | None = None
    terraform_source: str

    def source_with_ref(self) -> str:
        if self.latest_version:
            return f"git::{self.terraform_source}?ref={self.latest_version}"

        return f"git::{self.terraform_source}"