# Terraform Infrastructure

## Requirements

The following requirements are needed by this module:

- [terraform](#requirement_terraform) (>= 1.0)

- [aws](#requirement_aws) (~> 5.0)

## Providers

The following providers are used by this module:

- [aws](#provider_aws) (~> 5.0)

## Modules

No modules.

## Resources

The following resources are used by this module:

- [aws_api_gateway_rest_api.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/api_gateway_rest_api) (resource)
- [aws_cloudwatch_log_group.ecs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_log_group) (resource)
- [aws_db_subnet_group.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_subnet_group) (resource)
- [aws_ecs_cluster.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_cluster) (resource)
- [aws_ecs_service.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_service) (resource)
- [aws_ecs_task_definition.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/ecs_task_definition) (resource)
- [aws_eip.nat](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/eip) (resource)
- [aws_iam_role.ecs_exec](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) (resource)
- [aws_iam_role.ecs_task](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) (resource)
- [aws_iam_role_policy_attachment.ecs_exec_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) (resource)
- [aws_internet_gateway.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/internet_gateway) (resource)
- [aws_lb.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb) (resource)
- [aws_lb_listener.http](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_listener) (resource)
- [aws_lb_target_group.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lb_target_group) (resource)
- [aws_nat_gateway.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/nat_gateway) (resource)
- [aws_rds_cluster.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster) (resource)
- [aws_rds_cluster_instance.instance_1](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds_cluster_instance) (resource)
- [aws_route.private_nat](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route) (resource)
- [aws_route_table.private](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table) (resource)
- [aws_route_table_association.private_a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table_association) (resource)
- [aws_route_table_association.private_b](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/route_table_association) (resource)
- [aws_security_group.alb](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) (resource)
- [aws_security_group.ecs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) (resource)
- [aws_security_group.rds](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) (resource)
- [aws_subnet.private_a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet) (resource)
- [aws_subnet.private_b](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet) (resource)
- [aws_subnet.public_a](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/subnet) (resource)
- [aws_vpc.main](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc) (resource)
- [aws_vpc_security_group_ingress_rule.ecs_ingress](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc_security_group_ingress_rule) (resource)
- [aws_vpc_security_group_ingress_rule.rds_ingress](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc_security_group_ingress_rule) (resource)

## Required Inputs

No required inputs.

## Optional Inputs

The following input variables are optional (have default values):

### [aws_region](#input_aws_region)

Description: The AWS region to deploy resources into

Type: `string`

Default: `"us-east-1"`

### [environment](#input_environment)

Description: The environment name (e.g. dev, staging, prod)

Type: `string`

Default: `"production"`

### [project_name](#input_project_name)

Description: The name of the project

Type: `string`

Default: `"flurit-ai"`

## Outputs

The following outputs are exported:

### [alb_dns_name](#output_alb_dns_name)

Description: The DNS name of the Application Load Balancer

### [api_gateway_id](#output_api_gateway_id)

Description: The ID of the API Gateway

### [ecs_cluster_name](#output_ecs_cluster_name)

Description: The name of the ECS cluster

### [rds_cluster_endpoint](#output_rds_cluster_endpoint)

Description: The cluster endpoint for the RDS Aurora cluster

### [rds_cluster_reader_endpoint](#output_rds_cluster_reader_endpoint)

Description: The cluster reader endpoint for the RDS Aurora cluster

### [vpc_id](#output_vpc_id)

Description: The ID of the VPC

## Usage

```bash
terraform init
terraform plan
terraform apply
```
