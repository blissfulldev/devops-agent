variable "enabled" {
  type        = bool
  description = "Whether the distribution is enabled to accept end user requests for content"
  default     = true
}

variable "origin" {
  type        = any
  description = "One or more origins for this distribution"
}

variable "default_cache_behavior" {
  type        = any
  description = "The default cache behavior for this distribution"
}

variable "is_ipv6_enabled" {
  type        = bool
  description = "Whether the IPv6 is enabled for the distribution"
  default     = true
}

variable "price_class" {
  type        = string
  description = "The price class for this distribution"
  default     = "PriceClass_100"
}

variable "wait_for_deployment" {
  type        = bool
  description = "If enabled, the resource will wait for the distribution status to change from InProgress to Deployed"
  default     = true
}

variable "create_origin_access_control" {
  type        = bool
  description = "Whether to create Origin Access Control"
  default     = true
}

variable "origin_access_control" {
  type        = any
  description = "Map of CloudFront origin access control"
  default = {
    s3 = {
      signing_behavior = "always"
      origin_type      = "s3"
      signing_protocol = "sigv4"
    }
  }
}

