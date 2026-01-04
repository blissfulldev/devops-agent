module "eks" {
  source                   = "terraform-aws-modules/eks/aws"
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
  version = "21.10.1"
}

