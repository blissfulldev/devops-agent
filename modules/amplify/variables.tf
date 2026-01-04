variable "name" {
  type        = string
  description = "Name of the Amplify app"
}

variable "repository" {
  type        = string
  description = "The repository for the Amplify app"
}

variable "oauth_token" {
  type        = string
  description = "The OAuth token for a third-party source control system"
}

variable "platform" {
  type        = string
  description = "The platform or framework for the Amplify app"
  default     = "WEB"
}

variable "environment_variables" {
  type        = map(string)
  description = "The environment variables for the Amplify app"
}

