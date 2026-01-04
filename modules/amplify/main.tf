module "amplify" {
  source                = "cloudposse/amplify-app/aws"
  name                  = var.name
  repository            = var.repository
  oauth_token           = var.oauth_token
  platform              = var.platform
  environment_variables = var.environment_variables
  version               = "1.2.0"
}

