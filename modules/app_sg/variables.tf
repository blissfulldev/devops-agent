variable "name" {
  type        = string
  description = "Name of security group"
}

variable "vpc_id" {
  type        = string
  description = "ID of the VPC"
}

variable "computed_ingress_with_source_security_group_id" {
  type        = list(map(string))
  description = "List of computed ingress rules to create where 'source_security_group_id' is used"
}

variable "number_of_computed_ingress_with_source_security_group_id" {
  type        = number
  description = "Number of computed ingress rules to create where 'source_security_group_id' is used"
}

variable "egress_rules" {
  type        = list(string)
  description = "List of egress rules to create by name"
}

