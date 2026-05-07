resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/main-service"
  retention_in_days = 30
  tags              = local.common_tags
}
