# Terraform outputs for Agentic AI Solution

output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}

output "private_subnets" {
  description = "List of IDs of private subnets"
  value       = module.vpc.private_subnets
}

output "public_subnets" {
  description = "List of IDs of public subnets"
  value       = module.vpc.public_subnets
}

output "alb_dns_name" {
  description = "The DNS name of the load balancer"
  value       = aws_lb.agentic_ai.dns_name
}

output "alb_zone_id" {
  description = "The canonical hosted zone ID of the load balancer"
  value       = aws_lb.agentic_ai.zone_id
}

output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.agentic_ai.repository_url
}

output "ecr_repository_name" {
  description = "The name of the ECR repository"
  value       = aws_ecr_repository.agentic_ai.name
}

output "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  value       = aws_ecs_cluster.agentic_ai.name
}

output "ecs_cluster_arn" {
  description = "The ARN of the ECS cluster"
  value       = aws_ecs_cluster.agentic_ai.arn
}

output "ecs_service_name" {
  description = "The name of the ECS service"
  value       = aws_ecs_service.agentic_ai.name
}

output "ecs_service_arn" {
  description = "The ARN of the ECS service"
  value       = aws_ecs_service.agentic_ai.id
}

output "efs_file_system_id" {
  description = "The ID of the EFS file system"
  value       = aws_efs_file_system.agentic_ai.id
}

output "efs_access_point_id" {
  description = "The ID of the EFS access point"
  value       = aws_efs_access_point.agentic_ai.id
}

output "cloudwatch_log_group_name" {
  description = "The name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.agentic_ai.name
}

output "application_url" {
  description = "The URL where the application is accessible"
  value       = "http://${aws_lb.agentic_ai.dns_name}"
}

output "api_documentation_url" {
  description = "The URL for the API documentation"
  value       = "http://${aws_lb.agentic_ai.dns_name}/docs"
}

output "health_check_url" {
  description = "The URL for the health check endpoint"
  value       = "http://${aws_lb.agentic_ai.dns_name}/health"
} 