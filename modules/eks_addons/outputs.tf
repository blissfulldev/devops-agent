output "aws_load_balancer_controller" {
  value       = module.eks_addons.aws_load_balancer_controller
  description = "Map of attributes of the Helm release and IRSA created"
}

