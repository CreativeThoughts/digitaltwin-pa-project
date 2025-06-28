# Terraform configuration for Agentic AI Solution on AWS ECS Fargate
# This creates all necessary AWS resources for the application

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "agentic-ai-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = var.environment
      Application = "agentic-ai-solution"
      ManagedBy   = "terraform"
    }
  }
}

# VPC and Networking
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "${var.project_name}-vpc"
  cidr = var.vpc_cidr
  
  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs
  
  enable_nat_gateway = true
  single_nat_gateway = false
  one_nat_gateway_per_az = true
  
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Environment = var.environment
  }
}

# ECR Repository
resource "aws_ecr_repository" "agentic_ai" {
  name                 = "agentic-ai-solution"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
  
  encryption_configuration {
    encryption_type = "AES256"
  }
  
  tags = {
    Name = "agentic-ai-solution"
  }
}

# ECR Lifecycle Policy
resource "aws_ecr_lifecycle_policy" "agentic_ai" {
  repository = aws_ecr_repository.agentic_ai.name
  
  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 30 images"
        selection = {
          tagStatus     = "tagged"
          tagPrefixList = ["v"]
          countType     = "imageCountMoreThan"
          countNumber   = 30
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# ECS Cluster
resource "aws_ecs_cluster" "agentic_ai" {
  name = "${var.project_name}-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = {
    Name = "${var.project_name}-cluster"
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "agentic_ai" {
  name              = "/ecs/agentic-ai-solution"
  retention_in_days = 30
  
  tags = {
    Name = "agentic-ai-logs"
  }
}

# EFS File System for persistent storage
resource "aws_efs_file_system" "agentic_ai" {
  creation_token = "agentic-ai-efs"
  encrypted       = true
  
  tags = {
    Name = "agentic-ai-efs"
  }
}

# EFS Mount Targets
resource "aws_efs_mount_target" "agentic_ai" {
  count           = length(var.private_subnet_cidrs)
  file_system_id  = aws_efs_file_system.agentic_ai.id
  subnet_id       = module.vpc.private_subnets[count.index]
  security_groups = [aws_security_group.efs.id]
}

# EFS Access Point
resource "aws_efs_access_point" "agentic_ai" {
  file_system_id = aws_efs_file_system.agentic_ai.id
  
  root_directory {
    path = "/agentic-ai"
    creation_info {
      owner_gid   = 1000
      owner_uid   = 1000
      permissions = "755"
    }
  }
  
  tags = {
    Name = "agentic-ai-access-point"
  }
}

# Security Groups
resource "aws_security_group" "ecs_tasks" {
  name_prefix = "agentic-ai-ecs-tasks-"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    protocol         = "tcp"
    from_port        = 8000
    to_port          = 8000
    cidr_blocks      = [var.vpc_cidr]
    ipv6_cidr_blocks = [module.vpc.vpc_ipv6_cidr_block]
  }
  
  egress {
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  
  tags = {
    Name = "agentic-ai-ecs-tasks-sg"
  }
}

resource "aws_security_group" "efs" {
  name_prefix = "agentic-ai-efs-"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    protocol         = "tcp"
    from_port        = 2049
    to_port          = 2049
    security_groups  = [aws_security_group.ecs_tasks.id]
  }
  
  egress {
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  
  tags = {
    Name = "agentic-ai-efs-sg"
  }
}

# Application Load Balancer
resource "aws_lb" "agentic_ai" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnets
  
  enable_deletion_protection = false
  
  tags = {
    Name = "${var.project_name}-alb"
  }
}

resource "aws_security_group" "alb" {
  name_prefix = "agentic-ai-alb-"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    protocol         = "tcp"
    from_port        = 80
    to_port          = 80
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  
  ingress {
    protocol         = "tcp"
    from_port        = 443
    to_port          = 443
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  
  egress {
    protocol         = "-1"
    from_port        = 0
    to_port          = 0
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  
  tags = {
    Name = "agentic-ai-alb-sg"
  }
}

# ALB Target Group
resource "aws_lb_target_group" "agentic_ai" {
  name        = "${var.project_name}-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "ip"
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 3
  }
  
  tags = {
    Name = "${var.project_name}-tg"
  }
}

# ALB Listener
resource "aws_lb_listener" "agentic_ai" {
  load_balancer_arn = aws_lb.agentic_ai.arn
  port              = "80"
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.agentic_ai.arn
  }
}

# IAM Roles
resource "aws_iam_role" "ecs_task_execution" {
  name = "${var.project_name}-ecs-task-execution-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "ecs_task" {
  name = "${var.project_name}-ecs-task-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# ECS Task Definition
resource "aws_ecs_task_definition" "agentic_ai" {
  family                   = "agentic-ai-solution"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn
  
  container_definitions = jsonencode([
    {
      name  = "agentic-ai-container"
      image = "${aws_ecr_repository.agentic_ai.repository_url}:latest"
      
      portMappings = [
        {
          containerPort = 8000
          protocol      = "tcp"
        }
      ]
      
      environment = [
        {
          name  = "API_HOST"
          value = "0.0.0.0"
        },
        {
          name  = "API_PORT"
          value = "8000"
        },
        {
          name  = "LOG_LEVEL"
          value = "INFO"
        },
        {
          name  = "OUTPUT_FILE_PATH"
          value = "/app/output/responses.json"
        },
        {
          name  = "MAX_CONVERSATION_TURNS"
          value = "10"
        },
        {
          name  = "TIMEOUT"
          value = "60"
        }
      ]
      
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.agentic_ai.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
      
      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
      
      mountPoints = [
        {
          sourceVolume  = "output-data"
          containerPath = "/app/output"
          readOnly      = false
        }
      ]
    }
  ])
  
  volume {
    name = "output-data"
    efs_volume_configuration {
      file_system_id          = aws_efs_file_system.agentic_ai.id
      root_directory          = "/"
      transit_encryption      = "ENABLED"
      transit_encryption_port = 2049
      
      authorization_config {
        iam = "ENABLED"
      }
    }
  }
  
  tags = {
    Name = "agentic-ai-task-definition"
  }
}

# ECS Service
resource "aws_ecs_service" "agentic_ai" {
  name            = "${var.project_name}-service"
  cluster         = aws_ecs_cluster.agentic_ai.id
  task_definition = aws_ecs_task_definition.agentic_ai.arn
  desired_count   = var.service_desired_count
  launch_type     = "FARGATE"
  platform_version = "LATEST"
  
  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = module.vpc.private_subnets
    assign_public_ip = false
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.agentic_ai.arn
    container_name   = "agentic-ai-container"
    container_port   = 8000
  }
  
  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }
  
  deployment_controller {
    type = "ECS"
  }
  
  depends_on = [aws_lb_listener.agentic_ai]
  
  tags = {
    Name = "${var.project_name}-service"
  }
}

# Auto Scaling
resource "aws_appautoscaling_target" "agentic_ai" {
  max_capacity       = var.service_max_count
  min_capacity       = var.service_min_count
  resource_id        = "service/${aws_ecs_cluster.agentic_ai.name}/${aws_ecs_service.agentic_ai.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "agentic_ai_cpu" {
  name               = "${var.project_name}-cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.agentic_ai.resource_id
  scalable_dimension = aws_appautoscaling_target.agentic_ai.scalable_dimension
  service_namespace  = aws_appautoscaling_target.agentic_ai.service_namespace
  
  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value = 70.0
  }
}

# Outputs
output "alb_dns_name" {
  description = "The DNS name of the load balancer"
  value       = aws_lb.agentic_ai.dns_name
}

output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.agentic_ai.repository_url
}

output "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  value       = aws_ecs_cluster.agentic_ai.name
}

output "ecs_service_name" {
  description = "The name of the ECS service"
  value       = aws_ecs_service.agentic_ai.name
} 