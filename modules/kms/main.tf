module "kms" {
  source      = "terraform-aws-modules/kms/aws"
  description = "EKS Secret Encryption Key"
  aliases = [
    "alias/eks-cluster-key"
  ]
  enable_key_rotation = true
  tags = {
    Environment = "prod"
  }
  version = "4.1.1"
}

