variable "aws_region" {
  type        = string
  description = "The AWS region to deploy resources into"
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "The environment name (e.g. dev, staging, prod)"
  default     = "production"
}

variable "project_name" {
  type        = string
  description = "The name of the project"
  default     = "flurit-ai"
}
