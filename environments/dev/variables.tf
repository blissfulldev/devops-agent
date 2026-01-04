variable "region" {
  type        = string
  description = "AWS region for resource deployment (e.g., us-east-1, eu-west-1)"
  default     = "ap-southeast-1"
  sensitive   = false
}

variable "media_bucket_name" {
  type        = string
  description = "Name of the S3 bucket for media"
  default     = "matrimonial-app-media"
}

variable "frontend_repo" {
  type        = string
  description = "Repository URL for the frontend application"
  default     = "https://github.com/my-org/matrimonial-frontend"
}

variable "github_oauth_token" {
  type        = string
  description = "OAuth token for Amplify to access the repository"
}

variable "db_name" {
  type        = string
  description = "Name of the database"
  default     = "matrimonial_db"
}

variable "db_username" {
  type        = string
  description = "Username for the database"
  default     = "db_user"
}

