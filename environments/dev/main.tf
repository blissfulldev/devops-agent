terraform {
  required_version = ">= 1.14.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.27.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.9"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.20"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

provider "helm" {
}

provider "kubernetes" {
}

module "vpc" {
  source = "../../modules/vpc"
  name   = "eks-vpc"
  cidr   = "10.0.0.0/16"
  azs = [
    "us-west-2a",
    "us-west-2b",
    "us-west-2c"
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
  enable_nat_gateway     = true
  one_nat_gateway_per_az = true
  enable_dns_hostnames   = true
  tags = {
    Environment = "prod"
    Project     = "eks-microservices"
  }
}

module "kms" {
  source      = "../../modules/kms"
  description = "EKS Secret Encryption Key"
  aliases = [
    "alias/eks-cluster-key"
  ]
  enable_key_rotation = true
  tags = {
    Environment = "prod"
  }
}

module "eks" {
  source                   = "../../modules/eks"
  name                     = var.cluster_name
  kubernetes_version       = "1.30"
  endpoint_public_access   = true
  enable_irsa              = true
  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.private_subnets
  create_kms_key           = true
  eks_managed_node_groups = {
    general = {
      min_size     = 1
      max_size     = 3
      desired_size = 2
      instance_types = [
        "t3.medium"
      ]
    }
  }
  tags = {
    Environment = "prod"
  }
}

module "eks_addons" {
  source                              = "../../modules/eks_addons"
  cluster_name                        = module.eks.cluster_name
  cluster_endpoint                    = module.eks.cluster_endpoint
  cluster_version                     = module.eks.cluster_version
  oidc_provider_arn                   = module.eks.oidc_provider_arn
  enable_aws_load_balancer_controller = true
  enable_metrics_server               = true
  tags = {
    Environment = "prod"
  }
}

module "ecr" {
  source                          = "../../modules/ecr"
  repository_name                 = var.app_name
  repository_image_scan_on_push   = true
  repository_image_tag_mutability = "IMMUTABLE"
  repository_lifecycle_policy     = jsonencode({ "rules" : [{ "rulePriority" : 1, "description" : "Keep last 30 images", "selection" : { "tagStatus" : "any", "countType" : "imageCountMoreThan", "countNumber" : 30 }, "action" : { "type" : "expire" } }] })
  tags = {
    Environment = "prod"
  }
}

