variable "cidr" {
  type        = string
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "azs" {
  type        = list(string)
  description = "Availability Zones"
  default     = ["us-west-2a", "us-west-2b", "us-west-2c"]
}

variable "private_subnets" {
  type        = list(string)
  description = "Private subnets for worker nodes"
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "public_subnets" {
  type        = list(string)
  description = "Public subnets for load balancers"
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

variable "database_subnets" {
  type        = list(string)
  description = "Database subnets for stateful storage"
  default     = ["10.0.201.0/24", "10.0.202.0/24", "10.0.203.0/24"]
}

variable "enable_nat_gateway" {
  type        = bool
  description = "Enable NAT Gateway for private internet access"
  default     = true
}

variable "one_nat_gateway_per_az" {
  type        = bool
  description = "One NAT Gateway per AZ for High Availability"
  default     = true
}

variable "enable_dns_hostnames" {
  type        = bool
  description = "Enable DNS hostnames"
  default     = true
}

