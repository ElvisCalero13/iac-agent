resource "aws_codebuild_project" "bootstrap" {
  name         = "${var.project_name}-${var.environment}-bootstrap"
  service_role = aws_iam_role.codebuild_role.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/standard:7.0"
    type         = "LINUX_CONTAINER"

    environment_variable {
      name  = "BOOTSTRAP_PUBLISHER"
      value = "s3"
    }

    environment_variable {
      name  = "BOOTSTRAP_S3_BUCKET"
      value = aws_s3_bucket.knowledge_artifacts.bucket
    }

    environment_variable {
      name  = "BOOTSTRAP_S3_PREFIX"
      value = "knowledge-base/${var.environment}"
    }

    environment_variable {
      name  = "AWS_REGION"
      value = var.aws_region
    }
  }

  source {
    type      = "GITHUB"
    location  = "https://github.com/ElvisCalero13/iac-agent.git"
    buildspec = "buildspecs/bootstrap.yml"
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}
