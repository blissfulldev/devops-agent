variable "region" {
  type        = string
  description = "AWS Region"
  default     = "us-west-2"
}

variable "cluster_name" {
  type        = string
  description = "Name of the EKS cluster"
  default     = "eks-microservices"
}

variable "app_name" {
  type        = string
  description = "Name of the ECR repository"
  default     = "microservice-app"
}

