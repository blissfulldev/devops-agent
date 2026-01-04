# matrimonial-app

Infrastructure for a matrimonial application on AWS including VPC, RDS PostgreSQL, EC2 ASG behind ALB, S3/CloudFront for media, and Amplify for frontend.

## Prerequisites

Before deploying this infrastructure, ensure you have:

- [Terraform](https://www.terraform.io/downloads) >= 1.14.0 installed
- AWS CLI configured with appropriate credentials
- AWS account with permissions to create the required resources

## Project Structure

```
.
├── modules/                    # Reusable module wrappers
│   └── vpc/
│       ├── main.tf           # Calls terraform-aws-modules/vpc/aws
│       ├── variables.tf
│       └── outputs.tf
│   └── alb_sg/
│       ├── main.tf           # Calls terraform-aws-modules/security-group/aws
│       ├── variables.tf
│       └── outputs.tf
│   └── app_sg/
│       ├── main.tf           # Calls terraform-aws-modules/security-group/aws
│       ├── variables.tf
│       └── outputs.tf
│   └── db_sg/
│       ├── main.tf           # Calls terraform-aws-modules/security-group/aws
│       ├── variables.tf
│       └── outputs.tf
│   └── rds/
│       ├── main.tf           # Calls terraform-aws-modules/rds/aws
│       ├── variables.tf
│       └── outputs.tf
│   └── alb/
│       ├── main.tf           # Calls terraform-aws-modules/alb/aws
│       ├── variables.tf
│       └── outputs.tf
│   └── asg/
│       ├── main.tf           # Calls terraform-aws-modules/autoscaling/aws
│       ├── variables.tf
│       └── outputs.tf
│   └── s3_media/
│       ├── main.tf           # Calls terraform-aws-modules/s3-bucket/aws
│       ├── variables.tf
│       └── outputs.tf
│   └── cloudfront/
│       ├── main.tf           # Calls terraform-aws-modules/cloudfront/aws
│       ├── variables.tf
│       └── outputs.tf
│   └── amplify/
│       ├── main.tf           # Calls cloudposse/amplify-app/aws
│       ├── variables.tf
│       └── outputs.tf
├── environments/               # Environment-specific configurations
│   └── dev/
├── README.md
└── .gitignore
```

## Modules

This infrastructure uses the following Terraform Registry modules:

### vpc

| Property | Value |
|----------|-------|
| Source | [`terraform-aws-modules/vpc/aws`](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws) |
| Version | `6.5.1` |
| Publisher | terraform-aws-modules ✅ Verified |

**Purpose:** VPC with public, private, and database subnets across 3 AZs

### alb_sg

| Property | Value |
|----------|-------|
| Source | [`terraform-aws-modules/security-group/aws`](https://registry.terraform.io/modules/terraform-aws-modules/security-group/aws) |
| Version | `5.3.1` |
| Publisher | terraform-aws-modules ✅ Verified |

**Purpose:** Security Group for ALB

### app_sg

| Property | Value |
|----------|-------|
| Source | [`terraform-aws-modules/security-group/aws`](https://registry.terraform.io/modules/terraform-aws-modules/security-group/aws) |
| Version | `5.3.1` |
| Publisher | terraform-aws-modules ✅ Verified |

**Purpose:** Security Group for Application Instances

### db_sg

| Property | Value |
|----------|-------|
| Source | [`terraform-aws-modules/security-group/aws`](https://registry.terraform.io/modules/terraform-aws-modules/security-group/aws) |
| Version | `5.3.1` |
| Publisher | terraform-aws-modules ✅ Verified |

**Purpose:** Security Group for RDS

### rds

| Property | Value |
|----------|-------|
| Source | [`terraform-aws-modules/rds/aws`](https://registry.terraform.io/modules/terraform-aws-modules/rds/aws) |
| Version | `7.0.0` |
| Publisher | terraform-aws-modules ✅ Verified |

**Purpose:** RDS PostgreSQL Instance

### alb

| Property | Value |
|----------|-------|
| Source | [`terraform-aws-modules/alb/aws`](https://registry.terraform.io/modules/terraform-aws-modules/alb/aws) |
| Version | `10.4.0` |
| Publisher | terraform-aws-modules ✅ Verified |

**Purpose:** Application Load Balancer

### asg

| Property | Value |
|----------|-------|
| Source | [`terraform-aws-modules/autoscaling/aws`](https://registry.terraform.io/modules/terraform-aws-modules/autoscaling/aws) |
| Version | `9.0.2` |
| Publisher | terraform-aws-modules ✅ Verified |

**Purpose:** Auto Scaling Group for Backend

### s3_media

| Property | Value |
|----------|-------|
| Source | [`terraform-aws-modules/s3-bucket/aws`](https://registry.terraform.io/modules/terraform-aws-modules/s3-bucket/aws) |
| Version | `5.9.1` |
| Publisher | terraform-aws-modules ✅ Verified |

**Purpose:** S3 Bucket for Media Storage

### cloudfront

| Property | Value |
|----------|-------|
| Source | [`terraform-aws-modules/cloudfront/aws`](https://registry.terraform.io/modules/terraform-aws-modules/cloudfront/aws) |
| Version | `6.0.2` |
| Publisher | terraform-aws-modules ✅ Verified |

**Purpose:** CloudFront Distribution for Media

### amplify

| Property | Value |
|----------|-------|
| Source | [`cloudposse/amplify-app/aws`](https://registry.terraform.io/modules/cloudposse/amplify-app/aws) |
| Version | `1.2.0` |
| Publisher | cloudposse ✅ Verified |

**Purpose:** Amplify App for Frontend

## Additional Resources

The following resources are created directly (no suitable module available):

| Resource | Type | Reason |
|----------|------|--------|
| `amazon_linux_2023` | `aws_ami` | To get the latest Amazon Linux 2023 AMI ID for the ASG |

## Deployment

### Quick Start

```bash
# Navigate to the desired environment
cd environments/dev

# Initialize Terraform (downloads providers and modules)
terraform init

# Review the execution plan
terraform plan

# Apply the configuration
terraform apply
```

### Deploying to Different Environments

Each environment has its own configuration in `environments/<env>/`:

```bash
# Development
cd environments/dev && terraform init && terraform apply
```

## Variables Reference

| Name | Type | Description | Required | Default |
|------|------|-------------|----------|---------|
| `media_bucket_name` | `string` | Name of the S3 bucket for media | No | `"matrimonial-app-media"` |
| `frontend_repo` | `string` | Repository URL for the frontend application | No | `"https://github.com/my-org/...` |
| `github_oauth_token` | `string` | OAuth token for Amplify to access the repository | No | `null` |
| `db_name` | `string` | Name of the database | No | `"matrimonial_db"` |
| `db_username` | `string` | Username for the database | No | `"db_user"` |

🔒 = Sensitive variable

## Outputs

After successful deployment, the following outputs will be available:

| Name | Description |
|------|-------------|
| `vpc_id` | VPC ID |
| `db_endpoint` | Database Endpoint |
| `alb_dns_name` | ALB DNS Name |
| `cloudfront_domain_name` | CloudFront Domain Name |
| `amplify_default_domain` | Amplify Default Domain |

Access outputs after deployment:

```bash
terraform output

# Get a specific output
terraform output vpc_id
```

## Cleanup

To destroy all resources created by this configuration:

```bash
cd environments/<env>
terraform destroy
```

⚠️ **Warning:** This will permanently delete all resources. Review the plan carefully before confirming.

## CI/CD with GitHub Actions

This project includes a GitHub Actions workflow for automated infrastructure deployment.

### Workflow Location

```
.github/workflows/terraform-provision.yml
```

### Required GitHub Secrets & Variables

Configure these in your repository: **Settings → Secrets and variables → Actions**

#### AWS Configuration

| Type | Name | Description | Required |
|------|------|-------------|----------|
| Secret | `AWS_IAC_ROLE_ARN` | IAM role ARN for GitHub OIDC authentication | ✅ Yes |
| Variable | `AWS_REGION` | AWS region for deployment (default: us-east-1) | No |

#### AWS Setup Steps

1. **Create GitHub OIDC Provider** (one-time per AWS account):
   ```bash
   aws iam create-open-id-connect-provider \
     --url https://token.actions.githubusercontent.com \
     --client-id-list sts.amazonaws.com \
     --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
   ```

2. **Create IAM Role** with trust policy for your repository

3. **Attach Permissions** - the role needs permissions for all resources in this project

4. **Add Secret to GitHub**:
   ```bash
   gh secret set AWS_IAC_ROLE_ARN --body "arn:aws:iam::ACCOUNT_ID:role/YourRoleName"
   ```

📚 [Full AWS OIDC Setup Guide](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)

### Running the Workflow

The workflow can be triggered:
- **Automatically** on push to `main` branch
- **Manually** via GitHub Actions UI (workflow_dispatch)

```bash
# Trigger manually via GitHub CLI
gh workflow run terraform-provision.yml -f environment=dev
```

---

*Generated by Flurit [AI](https://www.flurit.ai)*