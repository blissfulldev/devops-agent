module "s3_media" {
  source                  = "terraform-aws-modules/s3-bucket/aws"
  bucket                  = var.bucket
  create_bucket           = var.create_bucket
  block_public_acls       = var.block_public_acls
  block_public_policy     = var.block_public_policy
  ignore_public_acls      = var.ignore_public_acls
  restrict_public_buckets = var.restrict_public_buckets
  version                 = "5.9.1"
}

