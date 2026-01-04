variable "name" {
  type        = string
  description = "Name of the ASG"
}

variable "min_size" {
  type        = number
  description = "The minimum size of the autoscaling group"
  default     = 1
}

variable "max_size" {
  type        = number
  description = "The maximum size of the autoscaling group"
  default     = 3
}

variable "desired_capacity" {
  type        = number
  description = "The number of Amazon EC2 instances that should be running in the autoscaling group"
  default     = 2
}

variable "vpc_zone_identifier" {
  type        = list(string)
  description = "A list of subnet IDs to launch resources in"
}

variable "security_groups" {
  type        = list(string)
  description = "A list of security group IDs to associate"
}

variable "instance_type" {
  type        = string
  description = "The type of the instance"
  default     = "t3.medium"
}

variable "image_id" {
  type        = string
  description = "The AMI from which to launch the instance"
}

variable "target_group_arns" {
  type        = list(string)
  description = "Map of target group ARNs to attach to the Auto Scaling Group"
}

