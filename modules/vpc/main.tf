module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
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
  version = "6.5.1"
}

