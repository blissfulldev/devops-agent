# eks-microservices-cluster

Infrastructure for a microservices-based Kubernetes cluster on AWS, including VPC, EKS, Node Groups, KMS, and ECR.

## Architecture

This infrastructure is built using the following Terraform modules:

### vpc

- **Source**: `terraform-aws-modules/vpc/aws`
- **Version**: `6.5.1`
- **Publisher**: terraform-aws-modules
- **Verified**: ✅
- **Description**: Network foundation with public, private, and database subnets across 3 AZs.

### kms

- **Source**: `terraform-aws-modules/kms/aws`
- **Version**: `4.1.1`
- **Publisher**: terraform-aws-modules
- **Verified**: ✅
- **Description**: KMS Key for EKS Cluster Encryption

### eks

- **Source**: `terraform-aws-modules/eks/aws`
- **Version**: `21.10.1`
- **Publisher**: terraform-aws-modules
- **Verified**: ✅
- **Description**: EKS Cluster Control Plane and Managed Node Groups

### eks_addons

- **Source**: `aws-ia/eks-blueprints-addons/aws`
- **Version**: `1.23.0`
- **Publisher**: aws-ia
- **Verified**: ❌
- **Description**: Kubernetes Add-ons (Load Balancer Controller, etc.)

### ecr

- **Source**: `terraform-aws-modules/ecr/aws`
- **Version**: `3.1.0`
- **Publisher**: terraform-aws-modules
- **Verified**: ✅
- **Description**: Container Registry for Microservices

## Variables

| Name | Type | Description | Default |
|------|------|-------------|---------|
| `region` | `string` | AWS Region | `"us-west-2"` |
| `cluster_name` | `string` | Name of the EKS cluster | `"eks-microservices"` |
| `app_name` | `string` | Name of the ECR repository | `"microservice-app"` |

## Outputs

| Name | Description |
|------|-------------|
| `vpc_id` | The ID of the VPC |
| `cluster_endpoint` | The endpoint for the EKS cluster |
| `ecr_repository_url` | The URL of the ECR repository |

## Usage

```bash
# Initialize Terraform
terraform init

# Plan the deployment
terraform plan

# Apply the configuration
terraform apply
```

## Generation Info

- **Generated**: 2026-01-02T17:57:07.469Z
- **MCP Tools Used**: terraform_search_modules, terraform_get_latest_module_version, terraform_get_module_details
- **Research Summary**: Selected official terraform-aws-modules for core components (VPC, EKS, KMS, ECR) due to their high usage, verification, and feature completeness. Selected aws-ia/eks-blueprints-addons for managing Kubernetes add-ons as it is the AWS recommended best practice.