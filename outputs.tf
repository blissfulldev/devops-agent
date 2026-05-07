output "vpc_id" {
  value       = aws_vpc.main.id
  description = "The ID of the VPC"
}

output "api_gateway_id" {
  value       = aws_api_gateway_rest_api.main.id
  description = "The ID of the API Gateway"
}

output "alb_dns_name" {
  value       = aws_lb.main.dns_name
  description = "The DNS name of the Application Load Balancer"
}

output "ecs_cluster_name" {
  value       = aws_ecs_cluster.main.name
  description = "The name of the ECS cluster"
}

output "rds_cluster_endpoint" {
  value       = aws_rds_cluster.main.endpoint
  description = "The cluster endpoint for the RDS Aurora cluster"
}

output "rds_cluster_reader_endpoint" {
  value       = aws_rds_cluster.main.reader_endpoint
  description = "The cluster reader endpoint for the RDS Aurora cluster"
}
