variable "identifier" {
  type        = string
  description = "The name of the RDS instance"
}

variable "engine" {
  type        = string
  description = "The database engine to use"
  default     = "postgres"
}

variable "engine_version" {
  type        = string
  description = "The engine version to use"
  default     = "14"
}

variable "family" {
  type        = string
  description = "The family of the DB parameter group"
  default     = "postgres14"
}

variable "major_engine_version" {
  type        = string
  description = "Specifies the major version of the engine that this option group should be associated with"
  default     = "14"
}

variable "instance_class" {
  type        = string
  description = "The instance type of the RDS instance"
  default     = "db.t3.large"
}

variable "allocated_storage" {
  type        = number
  description = "The allocated storage in gigabytes"
  default     = 20
}

variable "db_name" {
  type        = string
  description = "The DB name to create"
  default     = "matrimonial"
}

variable "username" {
  type        = string
  description = "Username for the master DB user"
  default     = "postgres"
}

variable "port" {
  type        = number
  description = "The port on which the DB accepts connections"
  default     = 5432
}

variable "multi_az" {
  type        = bool
  description = "Specifies if the RDS instance is multi-AZ"
  default     = true
}

variable "vpc_security_group_ids" {
  type        = list(string)
  description = "List of VPC security groups to associate"
}

variable "db_subnet_group_name" {
  type        = string
  description = "Name of DB subnet group"
}

variable "deletion_protection" {
  type        = bool
  description = "The database can't be deleted when this value is set to true"
  default     = true
}

