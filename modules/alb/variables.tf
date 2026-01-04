variable "name" {
  type        = string
  description = "The name of the LB"
}

variable "load_balancer_type" {
  type        = string
  description = "The type of load balancer to create"
  default     = "application"
}

variable "vpc_id" {
  type        = string
  description = "Identifier of the VPC"
}

variable "subnets" {
  type        = list(string)
  description = "A list of subnet IDs to attach to the LB"
}

variable "security_groups" {
  type        = list(string)
  description = "A list of security group IDs to assign to the LB"
}

variable "listeners" {
  type        = any
  description = "Map of listener configurations to create"
}

variable "target_groups" {
  type        = any
  description = "Map of target group configurations to create"
}

