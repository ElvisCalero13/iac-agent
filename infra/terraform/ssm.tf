resource "aws_ssm_parameter" "repositories_config" {
  name  = "/${var.project_name}/${var.environment}/repositories"
  type  = "SecureString"
  value = file("${path.module}/repositories.seed.json")

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}
