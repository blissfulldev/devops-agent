output "s3_bucket_id" {
  value       = module.s3_media.s3_bucket_id
  description = "The name of the bucket"
}

output "s3_bucket_arn" {
  value       = module.s3_media.s3_bucket_arn
  description = "The ARN of the bucket"
}

output "s3_bucket_bucket_domain_name" {
  value       = module.s3_media.s3_bucket_bucket_domain_name
  description = "The bucket domain name"
}

