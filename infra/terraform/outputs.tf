output "knowledge_artifacts_bucket" {
  value = aws_s3_bucket.knowledge_artifacts.bucket
}

output "github_token_secret_name" {
  value = aws_secretsmanager_secret.github_token.name
}

output "codebuild_project_name" {
  value = aws_codebuild_project.bootstrap.name
}
