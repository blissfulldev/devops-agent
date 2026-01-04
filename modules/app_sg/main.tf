module "app_sg" {
  source                                                   = "terraform-aws-modules/security-group/aws"
  name                                                     = var.name
  vpc_id                                                   = var.vpc_id
  computed_ingress_with_source_security_group_id           = var.computed_ingress_with_source_security_group_id
  number_of_computed_ingress_with_source_security_group_id = var.number_of_computed_ingress_with_source_security_group_id
  egress_rules                                             = var.egress_rules
  version                                                  = "5.3.1"
}

