module "ecr" {
  source                          = "terraform-aws-modules/ecr/aws"
  repository_name                 = var.app_name
  repository_image_scan_on_push   = true
  repository_image_tag_mutability = "IMMUTABLE"
  repository_lifecycle_policy     = jsonencode({ "rules" : [{ "rulePriority" : 1, "description" : "Keep last 30 images", "selection" : { "tagStatus" : "any", "countType" : "imageCountMoreThan", "countNumber" : 30 }, "action" : { "type" : "expire" } }] })
  tags = {
    Environment = "prod"
  }
  version = "3.1.0"
}

