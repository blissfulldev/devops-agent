variable "cluster_name" {
  type        = string
  description = "Name of the cluster"
  default     = "my-cluster"
}

variable "cluster_version" {
  type        = string
  description = "Kubernetes version"
  default     = "1.30"
}

variable "cluster_endpoint_public_access" {
  type        = bool
  description = "Enable public access to the cluster endpoint"
  default     = true
}

variable "enable_irsa" {
  type        = bool
  description = "Enable IRSA"
  default     = true
}

variable "vpc_id" {
  type        = string
  description = "VPC ID"
}

variable "subnet_ids" {
  type        = list(string)
  description = "Subnet IDs for the cluster"
}

variable "eks_managed_node_groups" {
  type        = any
  description = "Managed Node Groups configuration"
}

