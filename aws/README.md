# AWS ECS Fargate Deployment Guide

This guide provides step-by-step instructions for deploying the Agentic AI Solution to AWS ECS Fargate.

## 🏗️ Architecture Overview

The deployment includes:
- **ECS Fargate** - Serverless container orchestration
- **Application Load Balancer** - Traffic distribution and SSL termination
- **ECR** - Container image registry
- **EFS** - Persistent file storage
- **CloudWatch** - Logging and monitoring
- **Auto Scaling** - Automatic scaling based on CPU utilization
- **VPC** - Network isolation and security

## 📋 Prerequisites

1. **AWS CLI** installed and configured
2. **Docker** installed
3. **Terraform** installed (for infrastructure as code)
4. **AWS Account** with appropriate permissions
5. **Domain name** (optional, for custom domain)

## 🚀 Quick Start

### Option 1: Using Terraform (Recommended)

1. **Clone and setup the project:**
   ```bash
   git clone <your-repo>
   cd DigitalTwin-PA
   ```

2. **Configure Terraform:**
   ```bash
   cd aws/terraform
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your configuration
   ```

3. **Initialize Terraform:**
   ```bash
   terraform init
   ```

4. **Plan the deployment:**
   ```bash
   terraform plan
   ```

5. **Apply the infrastructure:**
   ```bash
   terraform apply
   ```

6. **Build and deploy the application:**
   ```bash
   cd ../..
   ./aws/deploy.sh deploy
   ```

### Option 2: Manual Deployment

1. **Build the Docker image:**
   ```bash
   docker build -t agentic-ai-solution .
   ```

2. **Create ECR repository:**
   ```bash
   aws ecr create-repository --repository-name agentic-ai-solution --region us-east-1
   ```

3. **Push to ECR:**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   docker tag agentic-ai-solution:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/agentic-ai-solution:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/agentic-ai-solution:latest
   ```

4. **Create ECS cluster and service using the provided JSON files**

## 🔧 Configuration

### Environment Variables

The application uses the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `OUTPUT_FILE_PATH` | Output file path | `/app/output/responses.json` |
| `MAX_CONVERSATION_TURNS` | Max conversation turns | `10` |
| `TIMEOUT` | Request timeout | `60` |

### AWS Resources

The Terraform configuration creates:

- **VPC** with public and private subnets
- **ECS Cluster** for container orchestration
- **ECR Repository** for container images
- **Application Load Balancer** for traffic distribution
- **EFS File System** for persistent storage
- **CloudWatch Log Group** for logging
- **IAM Roles** for ECS task execution
- **Security Groups** for network security
- **Auto Scaling** policies

## 📊 Monitoring and Logging

### CloudWatch Logs

Logs are automatically sent to CloudWatch:
- **Log Group**: `/ecs/agentic-ai-solution`
- **Retention**: 30 days
- **Stream Prefix**: `ecs`

### Health Checks

The application includes health checks:
- **Endpoint**: `/health`
- **Interval**: 30 seconds
- **Timeout**: 5 seconds
- **Retries**: 3

### Auto Scaling

Auto scaling is configured based on CPU utilization:
- **Target**: 70% CPU utilization
- **Min Instances**: 1
- **Max Instances**: 10
- **Scale Up**: When CPU > 70%
- **Scale Down**: When CPU < 70%

## 🔒 Security

### Network Security

- **VPC**: Isolated network environment
- **Private Subnets**: ECS tasks run in private subnets
- **Security Groups**: Restrict traffic to necessary ports
- **NAT Gateways**: Allow outbound internet access

### Container Security

- **Non-root User**: Container runs as non-root user
- **Image Scanning**: ECR automatically scans for vulnerabilities
- **Encryption**: EFS and ECR use encryption at rest
- **IAM Roles**: Least privilege access

### Secrets Management

For production, use AWS Secrets Manager for sensitive data:
```bash
# Store API keys in Secrets Manager
aws secretsmanager create-secret \
    --name "agentic-ai/autogen-api-key" \
    --description "AutoGen API Key" \
    --secret-string "your-api-key-here"
```

## 🚀 Deployment Scripts

### deploy.sh

The deployment script provides the following commands:

```bash
# Deploy the application
./aws/deploy.sh deploy

# Rollback to previous deployment
./aws/deploy.sh rollback

# Check service status
./aws/deploy.sh status
```

### Script Features

- **Prerequisites Check**: Validates Docker and AWS CLI
- **ECR Management**: Creates repository and handles authentication
- **Image Building**: Builds and tags Docker images
- **Service Updates**: Updates ECS service with new image
- **Health Monitoring**: Waits for service stability
- **Rollback Support**: Easy rollback to previous version

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to AWS ECS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push Docker image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: agentic-ai-solution
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster agentic-ai-cluster \
            --service agentic-ai-service \
            --force-new-deployment
```

## 🧪 Testing

### Local Testing

```bash
# Build and run locally
docker-compose up --build

# Test the API
curl http://localhost:8000/health
```

### Production Testing

```bash
# Get the load balancer URL
terraform output alb_dns_name

# Test health endpoint
curl http://<alb-dns-name>/health

# Test API documentation
curl http://<alb-dns-name>/docs
```

## 📈 Scaling

### Manual Scaling

```bash
# Scale up
aws ecs update-service \
    --cluster agentic-ai-cluster \
    --service agentic-ai-service \
    --desired-count 5

# Scale down
aws ecs update-service \
    --cluster agentic-ai-cluster \
    --service agentic-ai-service \
    --desired-count 2
```

### Auto Scaling

Auto scaling is automatically handled based on CPU utilization. You can adjust the scaling policies in the Terraform configuration.

## 🔧 Troubleshooting

### Common Issues

1. **Container fails to start**
   - Check CloudWatch logs
   - Verify environment variables
   - Check ECR image exists

2. **Health check failures**
   - Verify application is listening on port 8000
   - Check `/health` endpoint returns 200
   - Review security group rules

3. **High CPU/Memory usage**
   - Monitor CloudWatch metrics
   - Consider increasing task CPU/memory
   - Review application performance

### Useful Commands

```bash
# Check ECS service status
aws ecs describe-services \
    --cluster agentic-ai-cluster \
    --services agentic-ai-service

# View CloudWatch logs
aws logs tail /ecs/agentic-ai-solution --follow

# Check ALB target health
aws elbv2 describe-target-health \
    --target-group-arn <target-group-arn>
```

## 💰 Cost Optimization

### Resource Sizing

- **CPU**: Start with 1024 (1 vCPU) and adjust based on usage
- **Memory**: Start with 2048 MB and adjust based on usage
- **Instances**: Use auto scaling to minimize idle instances

### Cost Monitoring

- Set up CloudWatch billing alerts
- Monitor ECS service metrics
- Review and optimize resource allocation

## 🆘 Support

For issues and questions:
1. Check CloudWatch logs for application errors
2. Review ECS service events
3. Verify infrastructure with Terraform
4. Test locally with Docker Compose

## 📚 Additional Resources

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Docker Documentation](https://docs.docker.com/) 