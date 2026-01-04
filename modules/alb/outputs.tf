output "dns_name" {
  value       = module.alb.dns_name
  description = "The DNS name of the load balancer"
}

output "zone_id" {
  value       = module.alb.zone_id
  description = "The zone_id of the load balancer"
}

output "target_groups" {
  value       = module.alb.target_groups
  description = "Map of target groups created"
}

