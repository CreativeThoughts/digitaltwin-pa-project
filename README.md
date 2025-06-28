# Agentic AI Solution with AutoGen Framework

A multi-agent orchestration system built with AutoGen framework and FastAPI, designed for scalable expert agent management.

## Architecture

### Core Components

1. **Principal Agent** - Main orchestrator that receives requests and delegates to appropriate expert agents
2. **Expert Agents**:
   - Utility Management Expert
   - Financial Health Check Expert  
   - Vehicle Management Expert
3. **FastAPI Interface** - REST API endpoint for request ingestion
4. **File Streamer** - Output handler (temporary, will be replaced with API)

### Key Features

- **Modular Design**: Easy to add new expert agents without breaking existing functionality
- **Async Processing**: Non-blocking request handling with acknowledgment responses
- **Extensible Architecture**: Clean separation of concerns for future enhancements
- **Configurable**: Environment-based configuration for different deployment scenarios

## 🐳 Containerization & AWS Deployment

This solution is fully containerized and ready for deployment on AWS ECS Fargate with enterprise-grade infrastructure.

### 🚀 Quick Deployment

#### Option 1: Terraform (Recommended)
```bash
# Deploy infrastructure
cd aws/terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your configuration
terraform init
terraform plan
terraform apply

# Deploy application
cd ../..
./aws/deploy.sh deploy
```

#### Option 2: Docker Compose (Local Development)
```bash
# Build and run locally
docker-compose up --build

# Test the API
curl http://localhost:8000/health
```

### ☁️ AWS Infrastructure

The solution includes complete infrastructure as code with:

- **ECS Fargate** - Serverless container orchestration
- **Application Load Balancer** - Traffic distribution and SSL termination
- **ECR** - Container image registry with vulnerability scanning
- **EFS** - Persistent file storage with encryption
- **CloudWatch** - Comprehensive logging and monitoring
- **Auto Scaling** - Automatic scaling based on CPU utilization (1-10 instances)
- **VPC** - Network isolation and security
- **IAM Roles** - Least privilege access control

### 🔧 Key Benefits

#### 1. **Scalability** 🚀
- **Auto-scaling** from 1 to 10 instances based on demand
- **Load balancer** for intelligent traffic distribution
- **Multi-AZ deployment** for high availability across availability zones
- **Horizontal scaling** with zero-downtime deployments

#### 2. **Reliability** 🛡️
- **Health checks** and auto-recovery from failures
- **Circuit breakers** for deployment safety and rollback
- **Multi-AZ redundancy** for fault tolerance
- **Graceful degradation** and error handling

#### 3. **Security** 🔒
- **VPC isolation** with private subnets for ECS tasks
- **Security groups** with minimal required access
- **Encryption** at rest (EFS) and in transit (TLS)
- **IAM roles** with least privilege access principles
- **Non-root container** execution for enhanced security

#### 4. **Monitoring & Observability** 📊
- **CloudWatch logs** with structured logging and 30-day retention
- **Application health** monitoring with `/health` endpoint
- **Performance metrics** (CPU, Memory, Network)
- **Custom dashboards** for application monitoring
- **Proactive alerting** and notification capabilities

#### 5. **Cost Efficiency** 💰
- **Fargate** (serverless, pay-per-use, no idle costs)
- **Auto-scaling** (scale to zero when not needed)
- **Optimized resource** allocation and utilization
- **EFS lifecycle policies** for cost management
- **Slim container images** for faster deployments

#### 6. **Production Readiness** ✅
- **High availability** across multiple availability zones
- **Backup and recovery** capabilities with EFS
- **CI/CD integration** ready with GitHub Actions
- **Infrastructure as Code** with Terraform
- **Compliance** with AWS security best practices

### 📈 Performance Features

- **Load Balancing** with health checks and failover
- **Auto Scaling** based on CPU utilization (70% target)
- **Container optimization** for fast startup times
- **Efficient resource** utilization with Fargate
- **Monitoring** and alerting for performance optimization

### 🔄 Deployment Automation

The solution includes smart deployment scripts:

```bash
# Deploy to production
./aws/deploy.sh deploy

# Rollback if needed
./aws/deploy.sh rollback

# Check service status
./aws/deploy.sh status
```

### 🧪 Testing & Validation

- **Local testing** with Docker Compose
- **Health endpoint** validation (`/health`)
- **API documentation** at `/docs`
- **Load testing** capabilities
- **Integration testing** with AWS services

## 🚀 CI/CD Pipeline: GitHub Actions + AWS ECR/ECS

This project uses **GitHub Actions** for automated CI/CD, building and deploying Docker images to AWS ECS for both staging and production environments.

### Workflow Overview

- **CI**: Lint, test, and coverage on every push/PR (`.github/workflows/ci.yml`)
- **CD**:  
  - On push to `main`:
    - Build and push Docker image to AWS ECR
    - Deploy to ECS **staging** automatically
    - Deploy to ECS **production** after manual approval

### AWS & GitHub Setup

#### 1. AWS Resources Needed
- **ECR repository** for Docker images
- **ECS cluster** and **services** for staging and production
- **Task definition** with a container named `app`
- **IAM user** with permissions for ECR/ECS

#### 2. GitHub Environments & Secrets

Go to **GitHub → Settings → Environments** and create:
- `staging`
- `production`

For each environment, add these secrets:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION` (e.g., `us-east-1`)
- `ECR_REPOSITORY` (e.g., `123456789012.dkr.ecr.us-east-1.amazonaws.com/digitaltwin-pa`)
- `ECS_CLUSTER` (e.g., `digitaltwin-pa-cluster`)
- `ECS_SERVICE` (e.g., `digitaltwin-pa-staging-service` or `digitaltwin-pa-production-service`)
- `ECS_TASK_DEFINITION` (task definition family or ARN)
- (Optional for prod) `PRODUCTION_URL` (public URL for your production app)

#### 3. How Deployment Works

- **Staging**:  
  Every push to `main` automatically deploys the latest image to the staging ECS service.

- **Production**:  
  After a successful staging deploy, a manual approval step appears in the Actions tab. Once approved, the same image is deployed to production.

#### 4. Manual Approval

To deploy to production, go to the Actions tab, select the latest workflow run, and approve the "Wait for approval before deploying to production" step.

#### 5. Customization

- Adjust container name in `.github/workflows/cd.yml` if not `app`
- Add Slack/email notifications as needed
- Add health checks, migrations, or other steps as required

## Installation

### Local Development
```bash
pip install -r requirements.txt
```

### Containerized Deployment
```bash
# Build Docker image
docker build -t agentic-ai-solution .

# Run with Docker Compose
docker-compose up --build
```

## Usage

### Starting the Service

#### Local Development
```bash
python main.py
```

#### Containerized
```bash
docker-compose up --build
```

The FastAPI server will start on `http://localhost:8000`

### API Endpoints

- **POST** `/api/request` - Submit a new request for processing
- **GET** `/health` - Health check endpoint
- **GET** `/docs` - Interactive API documentation
- **GET** `/api/responses` - Retrieve recent responses
- **GET** `/api/agents/status` - Get agent status information

### Request Format

```json
{
  "request_id": "unique-request-id",
  "user_id": "user-identifier",
  "request_type": "utility_management|financial_health|vehicle_management|general",
  "description": "Detailed description of the request",
  "priority": "low|medium|high",
  "metadata": {
    "additional_data": "any additional context"
  }
}
```

## Project Structure

```
├── main.py                 # FastAPI application entry point
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Local development setup
├── setup.py               # Environment setup script
├── test_api.py            # API testing script
├── add_expert_agent.py    # Utility to add new expert agents
├── requirements.txt       # Python dependencies
├── config/
│   ├── __init__.py
│   └── settings.py        # Configuration management
├── agents/
│   ├── __init__.py
│   ├── base_agent.py      # Base agent class
│   ├── principal_agent.py # Main orchestrator agent
│   └── experts/
│       ├── __init__.py
│       ├── utility_agent.py
│       ├── financial_agent.py
│       └── vehicle_agent.py
├── api/
│   ├── __init__.py
│   ├── models.py          # Pydantic models
│   └── routes.py          # FastAPI routes
├── utils/
│   ├── __init__.py
│   ├── file_streamer.py   # Output handler
│   └── logger.py          # Logging utilities
├── aws/                   # AWS deployment configuration
│   ├── deploy.sh         # Deployment automation
│   ├── terraform/        # Infrastructure as Code
│   └── README.md         # AWS deployment guide
└── tests/
    └── __init__.py
```

## Adding New Expert Agents

1. Create a new agent class in `agents/experts/`
2. Inherit from `BaseExpertAgent`
3. Implement required methods
4. Register the agent in `PrincipalAgent`

Or use the automated script:
```bash
python add_expert_agent.py
```

## Environment Variables

Create a `.env` file with:

```
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
OUTPUT_FILE_PATH=./output/responses.json
```

## Future Enhancements

- Replace File Streamer with API endpoints
- Add authentication and authorization
- Implement agent performance monitoring
- Add support for complex workflows
- Integrate with external data sources
- Add Kubernetes deployment support
- Implement advanced monitoring with Prometheus/Grafana 

## API Documentation

### Interactive Documentation

- **Swagger UI**: Visit `http://localhost:8000/docs` for interactive API documentation
- **ReDoc**: Visit `http://localhost:8000/redoc` for alternative documentation view

### OpenAPI Specification

Download the complete OpenAPI 3.0 specification:

- **YAML Format**: [Download swagger.yaml](http://localhost:8000/swagger.yaml)
- **JSON Format**: Visit `http://localhost:8000/openapi.json`

You can import these files into:
- Postman or Insomnia for API testing
- Swagger UI for documentation
- Code generators for client libraries

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/request` | Submit request for processing |
| GET | `/api/responses` | Get recent responses |
| GET | `/api/agents/status` | Get agent status |
| POST | `/process` | Direct request processing |

## Key Benefits

### Containerization & AWS Deployment

- **Scalability**: Auto-scaling ECS services based on demand
- **Reliability**: Multi-AZ deployment with load balancing
- **Security**: VPC isolation, security groups, and IAM roles
- **Monitoring**: CloudWatch integration for metrics and logging
- **Cost Efficiency**: Pay-per-use model with auto-scaling
- **Production Ready**: Production-grade infrastructure with best practices

### Deployment Automation

- **Infrastructure as Code**: Complete AWS setup with Terraform
- **CI/CD Ready**: Automated deployment pipeline support
- **Environment Management**: Separate dev/staging/prod environments
- **Rollback Capability**: Easy rollback to previous versions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact: support@agentic-ai.com 