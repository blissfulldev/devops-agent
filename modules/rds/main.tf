module "rds" {
  source                 = "terraform-aws-modules/rds/aws"
  identifier             = var.identifier
  engine                 = var.engine
  engine_version         = var.engine_version
  family                 = var.family
  major_engine_version   = var.major_engine_version
  instance_class         = var.instance_class
  allocated_storage      = var.allocated_storage
  db_name                = var.db_name
  username               = var.username
  port                   = var.port
  multi_az               = var.multi_az
  vpc_security_group_ids = var.vpc_security_group_ids
  db_subnet_group_name   = var.db_subnet_group_name
  deletion_protection    = var.deletion_protection
  version                = "7.0.0"
}

