module "cloudfront" {
  source                       = "terraform-aws-modules/cloudfront/aws"
  enabled                      = var.enabled
  origin                       = var.origin
  default_cache_behavior       = var.default_cache_behavior
  is_ipv6_enabled              = var.is_ipv6_enabled
  price_class                  = var.price_class
  wait_for_deployment          = var.wait_for_deployment
  create_origin_access_control = var.create_origin_access_control
  origin_access_control        = var.origin_access_control
  version                      = "6.0.2"
}

