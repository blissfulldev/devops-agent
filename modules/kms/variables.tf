variable "description" {
  type        = string
  description = "Description of the key"
  default     = "EKS Secret Encryption Key"
}

variable "aliases" {
  type        = list(string)
  description = "Aliases for the key"
  default     = ["alias/eks-cluster-key"]
}

