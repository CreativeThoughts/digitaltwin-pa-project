from agents.quality_check_interface import QualityCheckInterface
from typing import Dict, Any, Optional
import autogen
from utils.logger import logger
from config.settings import settings
from agents.quality_check_interface import QualityReport, QualityMetric, QualityDimension
from abc import abstractmethod
from dataclasses import asdict

class BaseAgent(QualityCheckInterface):
    """Base class for all agents in the system with quality check capabilities."""
    
    def __init__(self, name: str, system_message: str, config_list: Optional[list] = None):
        """
        Initialize base agent.
        
        Args:
            name: Name of the agent
            system_message: System message for the agent
            config_list: AutoGen configuration list
        """
        self.name = name
        self.system_message = system_message
        self.config_list = config_list or settings.autogen_config_list
        self.agent = None
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the agent with AutoGen."""
        try:
            if self.config_list:
                self.agent = autogen.AssistantAgent(
                    name=self.name,
                    system_message=self.system_message,
                    llm_config={"config_list": self.config_list}
                )
            else:
                # Use default configuration for development
                self.agent = autogen.AssistantAgent(
                    name=self.name,
                    system_message=self.system_message
                )
            
            self.is_initialized = True
            logger.info(f"Agent {self.name} initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing agent {self.name}: {e}")
            raise
    
    @abstractmethod
    async def process(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a request and return results.
        
        Args:
            request_data: Request data dictionary
            
        Returns:
            Dictionary containing processing results
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information."""
        return {
            "name": self.name,
            "is_initialized": self.is_initialized,
            "type": self.__class__.__name__
        }
    
    async def cleanup(self):
        """Cleanup agent resources."""
        try:
            self.agent = None
            self.is_initialized = False
            logger.info(f"Agent {self.name} cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up agent {self.name}: {e}")
    
    def serialize_quality_report(self, quality_report: QualityReport) -> Dict[str, Any]:
        """Convert QualityReport to dictionary for serialization."""
        return asdict(quality_report)
    
    # Quality Check Interface Implementation
    def evaluate_quality(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityReport:
        """
        Evaluate the quality of agent results.
        
        Args:
            agent_result: The result/output from the agent
            original_request: The original request that was processed
            
        Returns:
            QualityReport: Comprehensive quality assessment
        """
        from datetime import datetime
        
        # Get quality metrics
        metrics = self.get_quality_metrics()
        
        # Assess each quality dimension
        assessed_metrics = []
        for metric in metrics:
            if metric.dimension == QualityDimension.ACCURACY:
                assessed_metrics.append(self.assess_accuracy(agent_result, original_request))
            elif metric.dimension == QualityDimension.COMPLETENESS:
                assessed_metrics.append(self.assess_completeness(agent_result, original_request))
            elif metric.dimension == QualityDimension.RELEVANCE:
                assessed_metrics.append(self.assess_relevance(agent_result, original_request))
            elif metric.dimension == QualityDimension.TIMELINESS:
                assessed_metrics.append(self.assess_timeliness(agent_result, original_request))
            elif metric.dimension == QualityDimension.CONSISTENCY:
                assessed_metrics.append(self.assess_consistency(agent_result, original_request))
            elif metric.dimension == QualityDimension.CLARITY:
                assessed_metrics.append(self.assess_clarity(agent_result, original_request))
            elif metric.dimension == QualityDimension.ACTIONABILITY:
                assessed_metrics.append(self.assess_actionability(agent_result, original_request))
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(assessed_metrics)
        
        # Determine if passed threshold
        threshold = self.get_quality_threshold()
        passed_threshold = overall_score >= threshold
        
        # Determine if approved for publication
        approved_for_publication = passed_threshold and overall_score >= 0.7
        
        # Generate summary
        summary = self.generate_summary(assessed_metrics, overall_score)
        
        # Calculate totals
        total_issues = sum(len(metric.issues) for metric in assessed_metrics)
        total_recommendations = sum(len(metric.recommendations) for metric in assessed_metrics)
        
        return QualityReport(
            agent_name=self.name,
            request_id=original_request.get("request_id", "unknown"),
            overall_score=overall_score,
            quality_level=self.determine_quality_level(overall_score),
            metrics=assessed_metrics,
            summary=summary,
            timestamp=datetime.utcnow(),
            passed_threshold=passed_threshold,
            approved_for_publication=approved_for_publication,
            total_issues=total_issues,
            total_recommendations=total_recommendations
        )
    
    def get_quality_threshold(self) -> float:
        """
        Get the minimum quality threshold for this agent.
        
        Returns:
            float: Minimum acceptable quality score (0.0 to 1.0)
        """
        return 0.6  # Default threshold - can be overridden by specific agents
    
    def get_quality_metrics(self) -> list[QualityMetric]:
        """
        Get the quality metrics configuration for this agent.
        
        Returns:
            List[QualityMetric]: List of quality metrics with weights
        """
        return [
            QualityMetric(QualityDimension.ACCURACY, 0.0, 0.3, "Accuracy assessment"),
            QualityMetric(QualityDimension.COMPLETENESS, 0.0, 0.2, "Completeness assessment"),
            QualityMetric(QualityDimension.RELEVANCE, 0.0, 0.2, "Relevance assessment"),
            QualityMetric(QualityDimension.TIMELINESS, 0.0, 0.1, "Timeliness assessment"),
            QualityMetric(QualityDimension.CONSISTENCY, 0.0, 0.1, "Consistency assessment"),
            QualityMetric(QualityDimension.CLARITY, 0.0, 0.05, "Clarity assessment"),
            QualityMetric(QualityDimension.ACTIONABILITY, 0.0, 0.05, "Actionability assessment")
        ]
    
    def _calculate_overall_score(self, metrics: list[QualityMetric]) -> float:
        """
        Calculate overall quality score from metrics.
        
        Args:
            metrics: List of quality metrics
            
        Returns:
            float: Overall quality score (0.0 to 1.0)
        """
        if not metrics:
            return 0.0
        
        total_weight = sum(metric.weight for metric in metrics)
        if total_weight == 0:
            return 0.0
        
        weighted_sum = sum(metric.score * metric.weight for metric in metrics)
        return weighted_sum / total_weight

class BaseExpertAgent(BaseAgent):
    """Base class for expert agents with specialized functionality and quality checks."""
    
    def __init__(self, name: str, system_message: str, expertise: str, config_list: Optional[list] = None):
        """
        Initialize expert agent.
        
        Args:
            name: Name of the agent
            system_message: System message for the agent
            expertise: Area of expertise
            config_list: AutoGen configuration list
        """
        super().__init__(name, system_message, config_list)
        self.expertise = expertise
        self.processing_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_processing_time": 0.0,
            "quality_scores": []
        }
    
    async def process(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process request with expert knowledge and quality evaluation.
        
        Args:
            request_data: Request data dictionary
            
        Returns:
            Dictionary containing expert analysis results with quality assessment
        """
        import time
        start_time = time.time()
        
        try:
            self.processing_stats["total_requests"] += 1
            
            # Validate request is appropriate for this expert
            if not self._can_handle_request(request_data):
                raise ValueError(f"Request type {request_data.get('request_type')} not suitable for {self.expertise} expert")
            
            # Process with expert knowledge
            result = await self._expert_process(request_data)
            
            # Update statistics
            processing_time = time.time() - start_time
            self.processing_stats["successful_requests"] += 1
            self.processing_stats["average_processing_time"] = (
                (self.processing_stats["average_processing_time"] * (self.processing_stats["successful_requests"] - 1) + processing_time) 
                / self.processing_stats["successful_requests"]
            )
            
            result["processing_time"] = processing_time
            result["expert_agent"] = self.name
            result["expertise"] = self.expertise
            
            # Perform quality evaluation
            quality_report = self.evaluate_quality(result, request_data)
            result["quality_report"] = self.serialize_quality_report(quality_report)
            
            # Store quality score for statistics
            self.processing_stats["quality_scores"].append(quality_report.overall_score)
            
            # Log quality assessment
            logger.info(f"Expert agent {self.name} processed request successfully in {processing_time:.2f}s")
            logger.info(f"Quality Score: {quality_report.overall_score:.2f} ({quality_report.quality_level.value})")
            
            if not quality_report.approved_for_publication:
                logger.warning(f"Quality threshold not met for {self.name}. Score: {quality_report.overall_score:.2f}")
            
            return result
            
        except Exception as e:
            self.processing_stats["failed_requests"] += 1
            logger.error(f"Error in expert agent {self.name}: {e}")
            raise
    
    @abstractmethod
    async def _expert_process(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implement expert-specific processing logic.
        
        Args:
            request_data: Request data dictionary
            
        Returns:
            Dictionary containing expert analysis results
        """
        pass
    
    def _can_handle_request(self, request_data: Dict[str, Any]) -> bool:
        """
        Check if this expert can handle the given request type.
        
        Args:
            request_data: Request data dictionary
            
        Returns:
            bool: True if can handle, False otherwise
        """
        request_type = request_data.get("request_type", "").lower()
        # Allow multi-domain/generic requests
        multi_domain_keywords = ["comprehensive_analysis", "multi_domain", "all", "general", "overview"]
        if any(keyword in request_type for keyword in multi_domain_keywords):
            return True
        return self.expertise.lower().replace(" ", "_") in request_type
    
    def get_status(self) -> Dict[str, Any]:
        """Get expert agent status with processing statistics and quality metrics."""
        base_status = super().get_status()
        
        # Calculate average quality score
        avg_quality = 0.0
        if self.processing_stats["quality_scores"]:
            avg_quality = sum(self.processing_stats["quality_scores"]) / len(self.processing_stats["quality_scores"])
        
        base_status.update({
            "expertise": self.expertise,
            "processing_stats": self.processing_stats,
            "average_quality_score": avg_quality
        })
        return base_status 