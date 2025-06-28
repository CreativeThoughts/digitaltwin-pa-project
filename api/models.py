from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime

class RequestType(str, Enum):
    """Enumeration of supported request types."""
    UTILITY_MANAGEMENT = "utility_management"
    FINANCIAL_HEALTH = "financial_health"
    VEHICLE_MANAGEMENT = "vehicle_management"
    GENERAL = "general"

class Priority(str, Enum):
    """Enumeration of request priorities."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RequestModel(BaseModel):
    """Model for incoming API requests."""
    request_id: str = Field(..., description="Unique identifier for the request")
    user_id: str = Field(..., description="Identifier of the user making the request")
    request_type: RequestType = Field(..., description="Type of request to be processed")
    description: str = Field(..., description="Detailed description of the request")
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority level of the request")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")

class ResponseModel(BaseModel):
    """Model for API responses."""
    request_id: str = Field(..., description="Request ID that was processed")
    status: str = Field(..., description="Status of the request processing")
    message: str = Field(..., description="Response message")
    timestamp: str = Field(..., description="Timestamp of the response")
    processing_id: Optional[str] = Field(None, description="Internal processing ID")

class HealthResponse(BaseModel):
    """Model for health check responses."""
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field(default="1.0.0", description="API version")

class AgentResponse(BaseModel):
    """Model for agent processing responses."""
    request_id: str
    agent_type: str
    status: str
    result: Dict[str, Any]
    processing_time: float
    timestamp: str

class QualityMetricModel(BaseModel):
    dimension: str
    score: float
    weight: float
    description: str
    issues: List[str]
    recommendations: List[str]

class QualityReportModel(BaseModel):
    agent_name: str
    request_id: str
    overall_score: float
    quality_level: str
    metrics: List[QualityMetricModel]
    summary: str
    timestamp: datetime
    passed_threshold: bool
    approved_for_publication: bool
    total_issues: int
    total_recommendations: int

class AgentResultModel(BaseModel):
    # You can add more fields as needed for your agent's result
    analysis_type: Optional[str]
    key_issues: Optional[List[str]]
    optimization_opportunities: Optional[List[str]]
    cost_savings_recommendations: Optional[List[str]]
    implementation_steps: Optional[List[str]]
    expected_benefits: Optional[List[str]]
    technology_recommendations: Optional[List[str]]
    priority_level: Optional[str]
    estimated_savings: Optional[str]
    implementation_timeline: Optional[str]
    quality_report: QualityReportModel
    # Add other fields as needed

class PrincipalAgentResponseModel(BaseModel):
    request_id: str
    processing_time: float
    principal_agent: str
    expert_results: Dict[str, AgentResultModel]
    quality_assessments: Dict[str, QualityReportModel]
    synthesis: Dict[str, Any]
    final_quality_report: QualityReportModel
    approved_for_publication: bool
    publication_status: str 