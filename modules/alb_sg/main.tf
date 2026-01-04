module "alb_sg" {
  source                   = "terraform-aws-modules/security-group/aws"
  name                     = var.name
  vpc_id                   = var.vpc_id
  ingress_rules            = var.ingress_rules
  ingress_with_cidr_blocks = var.ingress_with_cidr_blocks
  egress_with_cidr_blocks  = var.egress_with_cidr_blocks
  version                  = "5.3.1"
}

