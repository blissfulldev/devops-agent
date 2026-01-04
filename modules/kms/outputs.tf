output "key_arn" {
  value       = module.kms.key_arn
  description = "The ARN of the key"
}

output "key_id" {
  value       = module.kms.key_id
  description = "The globally unique identifier for the key"
}

