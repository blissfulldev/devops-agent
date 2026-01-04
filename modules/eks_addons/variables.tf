variable "cluster_name" {
  type        = string
  description = "Name of the EKS cluster"
}

variable "cluster_endpoint" {
  type        = string
  description = "Endpoint for your Kubernetes API server"
}

variable "cluster_version" {
  type        = string
  description = "Kubernetes version"
}

variable "oidc_provider_arn" {
  type        = string
  description = "The ARN of the cluster OIDC Provider"
}

variable "enable_aws_load_balancer_controller" {
  type        = bool
  description = "Enable AWS Load Balancer Controller"
  default     = true
}

variable "enable_metrics_server" {
  type        = bool
  description = "Enable Metrics Server"
  default     = true
}

