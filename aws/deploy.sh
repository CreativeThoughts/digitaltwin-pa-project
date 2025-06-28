#!/bin/bash

# AWS ECS Fargate Deployment Script for Agentic AI Solution
# This script builds the Docker image, pushes it to ECR, and deploys to ECS

set -e

# Configuration
AWS_REGION="us-east-1"
AWS_ACCOUNT_ID="YOUR_ACCOUNT_ID"
ECR_REPOSITORY="agentic-ai-solution"
ECS_CLUSTER="agentic-ai-cluster"
ECS_SERVICE="agentic-ai-service"
IMAGE_TAG="latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command_exists aws; then
        print_error "AWS CLI is not installed. Please install AWS CLI first."
        exit 1
    fi
    
    if ! aws sts get-caller-identity >/dev/null 2>&1; then
        print_error "AWS CLI is not configured. Please run 'aws configure' first."
        exit 1
    fi
    
    print_status "Prerequisites check passed."
}

# Create ECR repository if it doesn't exist
create_ecr_repository() {
    print_status "Checking ECR repository..."
    
    if ! aws ecr describe-repositories --repository-names "$ECR_REPOSITORY" --region "$AWS_REGION" >/dev/null 2>&1; then
        print_status "Creating ECR repository: $ECR_REPOSITORY"
        aws ecr create-repository \
            --repository-name "$ECR_REPOSITORY" \
            --region "$AWS_REGION" \
            --image-scanning-configuration scanOnPush=true \
            --encryption-configuration encryptionType=AES256
    else
        print_status "ECR repository already exists: $ECR_REPOSITORY"
    fi
}

# Get ECR login token
get_ecr_login() {
    print_status "Getting ECR login token..."
    aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
}

# Build Docker image
build_image() {
    print_status "Building Docker image..."
    
    # Build the image
    docker build -t "$ECR_REPOSITORY:$IMAGE_TAG" .
    
    # Tag for ECR
    docker tag "$ECR_REPOSITORY:$IMAGE_TAG" "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG"
    
    print_status "Docker image built successfully."
}

# Push image to ECR
push_image() {
    print_status "Pushing image to ECR..."
    docker push "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG"
    print_status "Image pushed to ECR successfully."
}

# Update ECS service
update_ecs_service() {
    print_status "Updating ECS service..."
    
    # Force new deployment
    aws ecs update-service \
        --cluster "$ECS_CLUSTER" \
        --service "$ECS_SERVICE" \
        --region "$AWS_REGION" \
        --force-new-deployment
    
    print_status "ECS service update initiated."
}

# Wait for service to be stable
wait_for_service_stability() {
    print_status "Waiting for service to be stable..."
    
    aws ecs wait services-stable \
        --cluster "$ECS_CLUSTER" \
        --services "$ECS_SERVICE" \
        --region "$AWS_REGION"
    
    print_status "Service is now stable."
}

# Get service status
get_service_status() {
    print_status "Getting service status..."
    
    aws ecs describe-services \
        --cluster "$ECS_CLUSTER" \
        --services "$ECS_SERVICE" \
        --region "$AWS_REGION" \
        --query 'services[0].{Status:status,RunningCount:runningCount,DesiredCount:desiredCount,PendingCount:pendingCount}' \
        --output table
}

# Main deployment function
deploy() {
    print_status "Starting deployment of Agentic AI Solution..."
    
    check_prerequisites
    create_ecr_repository
    get_ecr_login
    build_image
    push_image
    update_ecs_service
    wait_for_service_stability
    get_service_status
    
    print_status "Deployment completed successfully!"
    print_status "Your application should be available at your load balancer endpoint."
}

# Rollback function
rollback() {
    print_warning "Rolling back to previous deployment..."
    
    # Get the previous task definition
    PREVIOUS_TASK_DEF=$(aws ecs describe-services \
        --cluster "$ECS_CLUSTER" \
        --services "$ECS_SERVICE" \
        --region "$AWS_REGION" \
        --query 'services[0].taskDefinition' \
        --output text)
    
    # Update service to use previous task definition
    aws ecs update-service \
        --cluster "$ECS_CLUSTER" \
        --service "$ECS_SERVICE" \
        --region "$AWS_REGION" \
        --task-definition "$PREVIOUS_TASK_DEF" \
        --force-new-deployment
    
    wait_for_service_stability
    get_service_status
    
    print_status "Rollback completed."
}

# Show usage
usage() {
    echo "Usage: $0 [deploy|rollback|status]"
    echo ""
    echo "Commands:"
    echo "  deploy   - Build and deploy the application to ECS"
    echo "  rollback - Rollback to the previous deployment"
    echo "  status   - Show current service status"
    echo ""
    echo "Before running this script:"
    echo "1. Update AWS_ACCOUNT_ID in this script"
    echo "2. Ensure AWS CLI is configured"
    echo "3. Create the ECS cluster and service"
    echo "4. Set up the required IAM roles and security groups"
}

# Main script logic
case "${1:-deploy}" in
    deploy)
        deploy
        ;;
    rollback)
        rollback
        ;;
    status)
        get_service_status
        ;;
    *)
        usage
        exit 1
        ;;
esac 