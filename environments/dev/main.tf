terraform {
  required_version = ">= 1.14.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.27.0"
    }
  }
}

provider "aws" {
  region = var.region
}

module "vpc" {
  source = "../../modules/vpc"
  name   = "matrimonial-vpc"
  cidr   = "10.0.0.0/16"
  azs = [
    "us-east-1a",
    "us-east-1b",
    "us-east-1c"
  ]
  private_subnets = [
    "10.0.1.0/24",
    "10.0.2.0/24",
    "10.0.3.0/24"
  ]
  public_subnets = [
    "10.0.101.0/24",
    "10.0.102.0/24",
    "10.0.103.0/24"
  ]
  database_subnets = [
    "10.0.201.0/24",
    "10.0.202.0/24",
    "10.0.203.0/24"
  ]
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true
  enable_dns_support   = true
}

module "alb_sg" {
  source = "../../modules/alb_sg"
  name   = "matrimonial-alb-sg"
  vpc_id = module.vpc.vpc_id
  ingress_rules = [
    "https-443-tcp"
  ]
  ingress_cidr_blocks = [
    "0.0.0.0/0"
  ]
  egress_rules = [
    "all-all"
  ]
}

module "app_sg" {
  source = "../../modules/app_sg"
  name   = "matrimonial-app-sg"
  vpc_id = module.vpc.vpc_id
  ingress_with_source_security_group_id = [
    {
      from_port                = "80"
      to_port                  = "80"
      protocol                 = "tcp"
      source_security_group_id = module.alb_sg.security_group_id
    }
  ]
  egress_rules = [
    "all-all"
  ]
}

module "db_sg" {
  source = "../../modules/db_sg"
  name   = "matrimonial-db-sg"
  vpc_id = module.vpc.vpc_id
  ingress_with_source_security_group_id = [
    {
      from_port                = "5432"
      to_port                  = "5432"
      protocol                 = "tcp"
      source_security_group_id = module.app_sg.security_group_id
    }
  ]
}

module "rds" {
  source               = "../../modules/rds"
  identifier           = "matrimonial-db"
  engine               = "postgres"
  engine_version       = "14"
  family               = "postgres14"
  major_engine_version = "14"
  instance_class       = "db.t3.large"
  allocated_storage    = 20
  db_name              = var.db_name
  username             = var.db_username
  port                 = 5432
  multi_az             = true
  vpc_security_group_ids = [
    module.db_sg.security_group_id
  ]
  db_subnet_group_name = module.vpc.database_subnet_group
  deletion_protection  = true
}

module "alb" {
  source             = "../../modules/alb"
  name               = "matrimonial-alb"
  load_balancer_type = "application"
  vpc_id             = module.vpc.vpc_id
  subnets            = module.vpc.public_subnets
  security_groups = [
    module.alb_sg.security_group_id
  ]
}

module "asg" {
  source           = "../../modules/asg"
  iam_role_name    = "matrimonial-asg-role"
  min_size         = 1
  desired_capacity = 2
  image_id         = "ami-0c55b159cbfafe1f0"
  availability_zones = [
    "us-east-1a",
    "us-east-1b"
  ]
  security_groups = [
    module.app_sg.security_group_id
  ]
  availability_zone_distribution = {
    capacity_distribution_strategy = "balanced-best-effort"
  }
}

module "s3_media" {
  source                   = "../../modules/s3_media"
  bucket                   = var.media_bucket_name
  acl                      = "private"
  control_object_ownership = true
  object_ownership         = "BucketOwnerEnforced"
}

module "cloudfront" {
  source              = "../../modules/cloudfront"
  enabled             = true
  price_class         = "PriceClass_100"
  default_root_object = "index.html"
}

module "amplify" {
  source               = "../../modules/amplify"
  namespace            = "matrimonial"
  tenant               = "app"
  repository           = var.frontend_repo
  oauth_token          = var.github_oauth_token
  iam_service_role_arn = "arn:aws:iam::123456789012:role/amplify-role"
  additional_tag_map = {
  }
  null            = ""
  id_length_limit = 10
  domain_config = {
  }
}

