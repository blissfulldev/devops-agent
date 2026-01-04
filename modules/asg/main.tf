module "asg" {
  source              = "terraform-aws-modules/autoscaling/aws"
  name                = var.name
  min_size            = var.min_size
  max_size            = var.max_size
  desired_capacity    = var.desired_capacity
  vpc_zone_identifier = var.vpc_zone_identifier
  security_groups     = var.security_groups
  instance_type       = var.instance_type
  image_id            = var.image_id
  target_group_arns   = var.target_group_arns
  version             = "9.0.2"
}

