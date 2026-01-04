output "vpc_id" {
  value       = module.vpc.vpc_id
  description = "VPC ID"
}

output "db_endpoint" {
  value       = module.rds.db_instance_endpoint
  description = "Database Endpoint"
}

output "alb_dns_name" {
  value       = module.alb.dns_name
  description = "ALB DNS Name"
}

output "cloudfront_domain_name" {
  value       = module.cloudfront.cloudfront_distribution_domain_name
  description = "CloudFront Domain Name"
}

output "amplify_default_domain" {
  value       = module.amplify.default_domain
  description = "Amplify Default Domain"
}

