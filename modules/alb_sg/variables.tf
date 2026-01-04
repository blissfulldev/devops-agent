variable "name" {
  type        = string
  description = "Name of security group"
}

variable "vpc_id" {
  type        = string
  description = "ID of the VPC"
}

variable "ingress_rules" {
  type        = list(string)
  description = "List of ingress rules to create by name"
}

variable "ingress_with_cidr_blocks" {
  type        = list(map(string))
  description = "List of ingress rules to create where 'cidr_blocks' is used"
}

variable "egress_with_cidr_blocks" {
  type        = list(map(string))
  description = "List of egress rules to create where 'cidr_blocks' is used"
}

