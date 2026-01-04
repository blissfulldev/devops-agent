variable "repository_name" {
  type        = string
  description = "Name of the repository"
  default     = "my-app"
}

variable "repository_image_scan_on_push" {
  type        = bool
  description = "Scan images on push"
  default     = true
}

variable "repository_image_tag_mutability" {
  type        = string
  description = "Image tag mutability"
  default     = "IMMUTABLE"
}

