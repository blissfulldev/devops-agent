variable "cidr" {
  type        = string
  description = "The IPv4 CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "azs" {
  type        = list(string)
  description = "A list of availability zones names or ids in the region"
  default     = ["ap-southeast-1a", "ap-southeast-1b", "ap-southeast-1c"]
}

variable "private_subnets" {
  type        = list(string)
  description = "A list of private subnets inside the VPC"
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "public_subnets" {
  type        = list(string)
  description = "A list of public subnets inside the VPC"
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

variable "database_subnets" {
  type        = list(string)
  description = "A list of database subnets inside the VPC"
  default     = ["10.0.201.0/24", "10.0.202.0/24", "10.0.203.0/24"]
}

variable "enable_nat_gateway" {
  type        = bool
  description = "Should be true if you want to provision NAT Gateways for each of your private networks"
  default     = true
}

variable "single_nat_gateway" {
  type        = bool
  description = "Should be true if you want to provision a single shared NAT Gateway across all of your private networks"
  default     = true
}

variable "enable_dns_hostnames" {
  type        = bool
  description = "Should be true to enable DNS hostnames in the Default VPC"
  default     = true
}

variable "enable_dns_support" {
  type        = bool
  description = "Should be true to enable DNS support in the Default VPC"
  default     = true
}

