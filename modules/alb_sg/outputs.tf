output "security_group_id" {
  value       = module.alb_sg.security_group_id
  description = "The ID of the security group"
}

