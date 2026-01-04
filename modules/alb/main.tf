module "alb" {
  source             = "terraform-aws-modules/alb/aws"
  name               = var.name
  load_balancer_type = var.load_balancer_type
  vpc_id             = var.vpc_id
  subnets            = var.subnets
  security_groups    = var.security_groups
  listeners          = var.listeners
  target_groups      = var.target_groups
  version            = "10.4.0"
}

