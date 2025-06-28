from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class QualityScore(Enum):
    """Enumeration for quality scores."""
    EXCELLENT = "excellent"
    GOOD = "good"
    SATISFACTORY = "satisfactory"
    NEEDS_IMPROVEMENT = "needs_improvement"
    POOR = "poor"

class QualityDimension(Enum):
    """Enumeration for quality dimensions."""
    ACCURACY = "accuracy"
    COMPLETENESS = "completeness"
    RELEVANCE = "relevance"
    TIMELINESS = "timeliness"
    CONSISTENCY = "consistency"
    CLARITY = "clarity"
    ACTIONABILITY = "actionability"

@dataclass
class QualityMetric:
    """Data class for individual quality metrics."""
    dimension: QualityDimension
    score: float  # 0.0 to 1.0
    weight: float  # 0.0 to 1.0
    description: str
    issues: List[str] = None
    recommendations: List[str] = None
    
    def __post_init__(self):
        if self.issues is None:
            self.issues = []
        if self.recommendations is None:
            self.recommendations = []

@dataclass
class QualityReport:
    """Data class for comprehensive quality reports."""
    agent_name: str
    request_id: str
    overall_score: float  # 0.0 to 1.0
    quality_level: QualityScore
    metrics: List[QualityMetric]
    summary: str
    timestamp: datetime
    passed_threshold: bool
    approved_for_publication: bool
    total_issues: int
    total_recommendations: int
    
    def get_weighted_score(self) -> float:
        """Calculate weighted overall score."""
        if not self.metrics:
            return 0.0
        
        total_weight = sum(metric.weight for metric in self.metrics)
        if total_weight == 0:
            return 0.0
        
        weighted_sum = sum(metric.score * metric.weight for metric in self.metrics)
        return weighted_sum / total_weight

class QualityCheckInterface(ABC):
    """Abstract interface for quality checking that all agents must implement."""
    
    @abstractmethod
    def evaluate_quality(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityReport:
        """
        Evaluate the quality of agent results.
        
        Args:
            agent_result: The result/output from the agent
            original_request: The original request that was processed
            
        Returns:
            QualityReport: Comprehensive quality assessment
        """
        pass
    
    @abstractmethod
    def get_quality_threshold(self) -> float:
        """
        Get the minimum quality threshold for this agent.
        
        Returns:
            float: Minimum acceptable quality score (0.0 to 1.0)
        """
        pass
    
    @abstractmethod
    def get_quality_metrics(self) -> List[QualityMetric]:
        """
        Get the quality metrics configuration for this agent.
        
        Returns:
            List[QualityMetric]: List of quality metrics with weights
        """
        pass
    
    def assess_accuracy(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the accuracy of the agent's response.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Accuracy assessment
        """
        # Default implementation - should be overridden by specific agents
        return QualityMetric(
            dimension=QualityDimension.ACCURACY,
            score=0.5,  # Default score
            weight=0.3,
            description="Accuracy assessment not implemented for this agent",
            issues=["Accuracy assessment not customized"],
            recommendations=["Implement custom accuracy assessment"]
        )
    
    def assess_completeness(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the completeness of the agent's response.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Completeness assessment
        """
        # Default implementation - should be overridden by specific agents
        return QualityMetric(
            dimension=QualityDimension.COMPLETENESS,
            score=0.5,  # Default score
            weight=0.2,
            description="Completeness assessment not implemented for this agent",
            issues=["Completeness assessment not customized"],
            recommendations=["Implement custom completeness assessment"]
        )
    
    def assess_relevance(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the relevance of the agent's response.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Relevance assessment
        """
        # Default implementation - should be overridden by specific agents
        return QualityMetric(
            dimension=QualityDimension.RELEVANCE,
            score=0.5,  # Default score
            weight=0.2,
            description="Relevance assessment not implemented for this agent",
            issues=["Relevance assessment not customized"],
            recommendations=["Implement custom relevance assessment"]
        )
    
    def assess_timeliness(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the timeliness of the agent's response.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Timeliness assessment
        """
        processing_time = agent_result.get("processing_time", 0)
        
        # Define timeliness thresholds (in seconds)
        excellent_threshold = 5.0
        good_threshold = 15.0
        satisfactory_threshold = 30.0
        needs_improvement_threshold = 60.0
        
        if processing_time <= excellent_threshold:
            score = 1.0
            description = f"Excellent response time: {processing_time:.2f}s"
        elif processing_time <= good_threshold:
            score = 0.8
            description = f"Good response time: {processing_time:.2f}s"
        elif processing_time <= satisfactory_threshold:
            score = 0.6
            description = f"Satisfactory response time: {processing_time:.2f}s"
        elif processing_time <= needs_improvement_threshold:
            score = 0.4
            description = f"Response time needs improvement: {processing_time:.2f}s"
        else:
            score = 0.2
            description = f"Poor response time: {processing_time:.2f}s"
        
        issues = []
        recommendations = []
        
        if processing_time > good_threshold:
            issues.append(f"Response time ({processing_time:.2f}s) exceeds optimal threshold")
            recommendations.append("Consider optimizing agent processing logic")
        
        return QualityMetric(
            dimension=QualityDimension.TIMELINESS,
            score=score,
            weight=0.1,
            description=description,
            issues=issues,
            recommendations=recommendations
        )
    
    def assess_consistency(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the consistency of the agent's response.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Consistency assessment
        """
        # Default implementation - should be overridden by specific agents
        return QualityMetric(
            dimension=QualityDimension.CONSISTENCY,
            score=0.5,  # Default score
            weight=0.1,
            description="Consistency assessment not implemented for this agent",
            issues=["Consistency assessment not customized"],
            recommendations=["Implement custom consistency assessment"]
        )
    
    def assess_clarity(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the clarity of the agent's response.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Clarity assessment
        """
        # Default implementation - should be overridden by specific agents
        return QualityMetric(
            dimension=QualityDimension.CLARITY,
            score=0.5,  # Default score
            weight=0.05,
            description="Clarity assessment not implemented for this agent",
            issues=["Clarity assessment not customized"],
            recommendations=["Implement custom clarity assessment"]
        )
    
    def assess_actionability(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the actionability of the agent's response.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Actionability assessment
        """
        # Default implementation - should be overridden by specific agents
        return QualityMetric(
            dimension=QualityDimension.ACTIONABILITY,
            score=0.5,  # Default score
            weight=0.05,
            description="Actionability assessment not implemented for this agent",
            issues=["Actionability assessment not customized"],
            recommendations=["Implement custom actionability assessment"]
        )
    
    def determine_quality_level(self, score: float) -> QualityScore:
        """
        Determine quality level based on score.
        
        Args:
            score: Quality score (0.0 to 1.0)
            
        Returns:
            QualityScore: Quality level enum
        """
        if score >= 0.9:
            return QualityScore.EXCELLENT
        elif score >= 0.8:
            return QualityScore.GOOD
        elif score >= 0.7:
            return QualityScore.SATISFACTORY
        elif score >= 0.6:
            return QualityScore.NEEDS_IMPROVEMENT
        else:
            return QualityScore.POOR
    
    def generate_summary(self, metrics: List[QualityMetric], overall_score: float) -> str:
        """
        Generate a summary of the quality assessment.
        
        Args:
            metrics: List of quality metrics
            overall_score: Overall quality score
            
        Returns:
            str: Summary of the quality assessment
        """
        quality_level = self.determine_quality_level(overall_score)
        
        total_issues = sum(len(metric.issues) for metric in metrics)
        total_recommendations = sum(len(metric.recommendations) for metric in metrics)
        
        summary = f"Quality Assessment: {quality_level.value.upper()} (Score: {overall_score:.2f})\n"
        summary += f"Total Issues Found: {total_issues}\n"
        summary += f"Total Recommendations: {total_recommendations}\n"
        
        if total_issues == 0:
            summary += "No quality issues detected. Results are ready for publication."
        else:
            summary += f"Quality issues detected. Review recommended before publication."
        
        return summary 