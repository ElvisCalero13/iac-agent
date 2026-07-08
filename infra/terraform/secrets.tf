resource "aws_secretsmanager_secret" "github_token" {
  name = "${var.project_name}/${var.environment}/github-token"

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}
