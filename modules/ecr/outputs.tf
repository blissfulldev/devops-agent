output "repository_url" {
  value       = module.ecr.repository_url
  description = "The URL of the repository"
}

output "repository_arn" {
  value       = module.ecr.repository_arn
  description = "Full ARN of the repository"
}

