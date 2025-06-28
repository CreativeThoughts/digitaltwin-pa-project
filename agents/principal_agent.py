from typing import Dict, Any, List, Optional
import asyncio
from agents.base_agent import BaseAgent
from agents.experts.financial_agent import FinancialHealthExpert
from agents.experts.utility_agent import UtilityManagementExpert
from agents.experts.vehicle_agent import VehicleManagementExpert
from agents.quality_check_interface import QualityCheckInterface, QualityReport, QualityMetric, QualityDimension
from utils.logger import logger
from utils.file_streamer import FileStreamer
import autogen
from config.settings import settings
from dataclasses import asdict

class PrincipalAgent(BaseAgent):
    """Principal agent that orchestrates expert agents and ensures quality control."""
    
    def __init__(self, config_list: Optional[list] = None):
        """
        Initialize the principal agent with expert agents.
        
        Args:
            config_list: AutoGen configuration list
        """
        system_message = """You are a Principal Agent responsible for orchestrating multiple expert agents 
        in a digital twin system. Your role is to:
        1. Analyze incoming requests and determine which expert agents should handle them
        2. Coordinate the workflow between expert agents
        3. Synthesize results from multiple experts into a comprehensive response
        4. Ensure quality standards are met before publishing results
        5. Provide clear, actionable insights to users
        
        You have access to the following expert agents:
        - Financial Agent: Handles financial health checks, budget analysis, cost optimization
        - Utility Agent: Manages utility consumption, efficiency analysis, sustainability metrics
        - Vehicle Agent: Handles vehicle management, maintenance scheduling, fleet optimization
        
        Always ensure that the final response is comprehensive, accurate, and actionable."""
        
        super().__init__("PrincipalAgent", system_message, config_list)
        
        # Initialize expert agents
        self.expert_agents: Dict[str, BaseAgent] = {}
        self.workflow_history: List[Dict[str, Any]] = []
        self.file_streamer = FileStreamer()
        self.quality_reports = []
        self.publication_queue = []
    
    async def initialize(self):
        """Initialize the principal agent and all expert agents."""
        try:
            logger.info("[PrincipalAgent] Initializing principal agent...")
            # Initialize principal agent
            await super().initialize()
            logger.info(f"[PrincipalAgent] is_initialized after super(): {self.is_initialized}")
            
            # Initialize expert agents
            logger.info("[PrincipalAgent] Initializing expert agents...")
            self.expert_agents = {
                "financial": None,
                "utility": None,
                "vehicle": None
            }
            try:
                from agents.experts.financial_agent import FinancialHealthExpert
                self.expert_agents["financial"] = FinancialHealthExpert()
                logger.info("[PrincipalAgent] FinancialHealthExpert instance created")
            except Exception as e:
                logger.error(f"[PrincipalAgent] Error creating FinancialHealthExpert: {e}")
            try:
                from agents.experts.utility_agent import UtilityManagementExpert
                self.expert_agents["utility"] = UtilityManagementExpert()
                logger.info("[PrincipalAgent] UtilityManagementExpert instance created")
            except Exception as e:
                logger.error(f"[PrincipalAgent] Error creating UtilityManagementExpert: {e}")
            try:
                from agents.experts.vehicle_agent import VehicleManagementExpert
                self.expert_agents["vehicle"] = VehicleManagementExpert()
                logger.info("[PrincipalAgent] VehicleManagementExpert instance created")
            except Exception as e:
                logger.error(f"[PrincipalAgent] Error creating VehicleManagementExpert: {e}")
            
            # Remove any None values if instantiation failed
            self.expert_agents = {k: v for k, v in self.expert_agents.items() if v is not None}
            logger.info(f"[PrincipalAgent] Expert agents dict after instantiation: {self.expert_agents}")
            
            # Initialize all expert agents
            for name, agent in self.expert_agents.items():
                try:
                    logger.info(f"[PrincipalAgent] Initializing expert agent: {name}")
                    await agent.initialize()
                    logger.info(f"[PrincipalAgent] Expert agent {name} initialized")
                except Exception as e:
                    logger.error(f"[PrincipalAgent] Error initializing expert agent {name}: {e}")
            
            logger.info("Principal agent and all expert agents initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing principal agent: {e}")
            raise
    
    async def process(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a request by orchestrating expert agents and synthesizing results.
        
        Args:
            request_data: Request data dictionary
            
        Returns:
            Dictionary containing synthesized results and quality assessment
        """
        import time
        start_time = time.time()
        
        try:
            # Check if principal agent is initialized
            if not self.is_initialized:
                logger.error("Principal agent is not initialized. Please call initialize() first.")
                raise RuntimeError("Principal agent is not initialized")
            
            logger.info(f"Principal agent processing request: {request_data.get('request_type', 'unknown')}")
            
            # Step 1: Analyze request and determine required experts
            required_experts = self._determine_required_experts(request_data)
            logger.info(f"Required experts: {list(required_experts.keys())}")
            
            # Step 2: Delegate to expert agents
            expert_results = {}
            for expert_name, expert_agent in required_experts.items():
                try:
                    logger.info(f"Delegating to {expert_name} expert")
                    expert_result = await expert_agent.process(request_data)
                    expert_results[expert_name] = expert_result
                    logger.info(f"{expert_name} expert completed successfully")
                except Exception as e:
                    logger.error(f"Error in {expert_name} expert: {e}")
                    expert_results[expert_name] = {
                        "error": str(e),
                        "expert_agent": expert_name,
                        "status": "failed"
                    }
            
            # Step 3: Synthesize results
            synthesis_result = await self._synthesize_results(request_data, expert_results)
            
            # Step 4: Perform quality check on synthesis
            quality_report = self.evaluate_quality(synthesis_result, request_data)
            
            # Step 5: Prepare final response
            processing_time = time.time() - start_time
            final_response = {
                "request_id": request_data.get("request_id", "unknown"),
                "request_type": request_data.get("request_type", "unknown"),
                "status": "completed",
                "processing_time": processing_time,
                "principal_agent": self.name,
                "expert_results": expert_results,
                "synthesis": synthesis_result,
                "quality_report": self.serialize_quality_report(quality_report),
                "approved_for_publication": quality_report.approved_for_publication,
                "timestamp": time.time()
            }
            
            # Step 6: Log workflow
            self.workflow_history.append({
                "request_id": request_data.get("request_id", "unknown"),
                "timestamp": time.time(),
                "experts_used": list(required_experts.keys()),
                "quality_score": quality_report.overall_score,
                "approved": quality_report.approved_for_publication
            })
            
            logger.info(f"Principal agent completed processing in {processing_time:.2f}s")
            # Use string for quality_level in logging
            quality_level = quality_report.quality_level if isinstance(quality_report.quality_level, str) else getattr(quality_report.quality_level, 'value', str(quality_report.quality_level))
            logger.info(f"Quality Score: {quality_report.overall_score:.2f} ({quality_level})")
            
            if quality_report.approved_for_publication:
                logger.info("Results approved for publication")
                self.publication_queue.append(final_response)
                await self._publish_results(final_response)
            else:
                logger.warning("Results did not meet quality threshold for publication")
            
            return final_response
            
        except Exception as e:
            logger.error(f"Error in principal agent processing: {e}")
            raise
    
    def _determine_required_experts(self, request_data: Dict[str, Any]) -> Dict[str, BaseAgent]:
        """
        Determine which expert agents are required for the given request.
        
        Args:
            request_data: Request data dictionary
            
        Returns:
            Dictionary mapping expert names to agent instances
        """
        request_type = request_data.get("request_type", "").lower()
        required_experts = {}
        
        # Check if expert agents are available
        if not self.expert_agents:
            logger.warning("No expert agents available - principal agent may not be initialized")
            return required_experts
        
        # Financial-related requests
        if any(keyword in request_type for keyword in ["financial", "budget", "cost", "expense", "revenue", "profit"]):
            if "financial" in self.expert_agents:
                required_experts["financial"] = self.expert_agents["financial"]
        
        # Utility-related requests
        if any(keyword in request_type for keyword in ["utility", "energy", "water", "electricity", "consumption", "efficiency", "sustainability"]):
            if "utility" in self.expert_agents:
                required_experts["utility"] = self.expert_agents["utility"]
        
        # Vehicle-related requests
        if any(keyword in request_type for keyword in ["vehicle", "fleet", "maintenance", "transport", "logistics", "fuel"]):
            if "vehicle" in self.expert_agents:
                required_experts["vehicle"] = self.expert_agents["vehicle"]
        
        # If no specific type detected, use all experts for comprehensive analysis
        if not required_experts:
            logger.info("No specific expert type detected, using all experts for comprehensive analysis")
            required_experts = self.expert_agents.copy()
        
        return required_experts
    
    async def _synthesize_results(self, request_data: Dict[str, Any], expert_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize results from multiple expert agents into a comprehensive response.
        
        Args:
            request_data: Original request data
            expert_results: Results from expert agents
            
        Returns:
            Dictionary containing synthesized results
        """
        try:
            # Extract key insights from each expert
            insights = {}
            recommendations = []
            metrics = {}
            
            for expert_name, result in expert_results.items():
                if "error" not in result:
                    # Extract insights
                    if "insights" in result:
                        insights[expert_name] = result["insights"]
                    
                    # Extract recommendations
                    if "recommendations" in result:
                        recommendations.extend(result["recommendations"])
                    
                    # Extract metrics
                    if "metrics" in result:
                        metrics[expert_name] = result["metrics"]
            
            # Create synthesis
            synthesis = {
                "summary": f"Analysis completed by {len(expert_results)} expert agents",
                "insights": insights,
                "recommendations": recommendations,
                "metrics": metrics,
                "expert_count": len(expert_results),
                "successful_experts": len([r for r in expert_results.values() if "error" not in r]),
                "failed_experts": len([r for r in expert_results.values() if "error" in r])
            }
            
            return synthesis
            
        except Exception as e:
            logger.error(f"Error synthesizing results: {e}")
            return {
                "error": f"Failed to synthesize results: {str(e)}",
                "summary": "Synthesis failed"
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get principal agent status with expert agent information."""
        base_status = super().get_status()
        
        expert_statuses = {}
        for name, agent in self.expert_agents.items():
            expert_statuses[name] = agent.get_status()
        
        base_status.update({
            "expert_agents": expert_statuses,
            "workflow_history_count": len(self.workflow_history),
            "recent_workflows": self.workflow_history[-5:] if self.workflow_history else [],
            "publication_queue_size": len(self.publication_queue)
        })
        
        return base_status
    
    async def cleanup(self):
        """Cleanup principal agent and all expert agents."""
        try:
            # Cleanup expert agents
            for name, agent in self.expert_agents.items():
                await agent.cleanup()
                logger.info(f"Expert agent {name} cleaned up")
            
            # Cleanup principal agent
            await super().cleanup()
            
            logger.info("Principal agent and all expert agents cleaned up")
            
        except Exception as e:
            logger.error(f"Error cleaning up principal agent: {e}")
    
    # Quality Check Interface Implementation
    def get_quality_threshold(self) -> float:
        """Get quality threshold for principal agent synthesis."""
        return 0.7  # Higher threshold for synthesis
    
    def get_quality_metrics(self) -> list:
        """Get quality metrics for principal agent synthesis."""
        from agents.quality_check_interface import QualityMetric
        
        return [
            QualityMetric(QualityDimension.ACCURACY, 0.0, 0.25, "Synthesis accuracy"),
            QualityMetric(QualityDimension.COMPLETENESS, 0.0, 0.25, "Synthesis completeness"),
            QualityMetric(QualityDimension.RELEVANCE, 0.0, 0.2, "Synthesis relevance"),
            QualityMetric(QualityDimension.CONSISTENCY, 0.0, 0.15, "Cross-expert consistency"),
            QualityMetric(QualityDimension.CLARITY, 0.0, 0.1, "Synthesis clarity"),
            QualityMetric(QualityDimension.ACTIONABILITY, 0.0, 0.05, "Actionability of synthesis")
        ]
    
    def assess_accuracy(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """Assess accuracy of synthesis results."""
        from agents.quality_check_interface import QualityMetric, QualityDimension
        
        score = 0.8  # Base score for synthesis
        issues = []
        recommendations = []
        
        # Check if all expert results are present
        expert_results = agent_result.get("expert_results", {})
        if not expert_results:
            score -= 0.3
            issues.append("No expert results available for synthesis")
        
        # Check for failed experts
        failed_experts = [r for r in expert_results.values() if "error" in r]
        if failed_experts:
            score -= 0.2 * len(failed_experts)
            issues.append(f"{len(failed_experts)} expert(s) failed during processing")
        
        # Check synthesis quality
        synthesis = agent_result.get("synthesis", {})
        if "error" in synthesis:
            score -= 0.4
            issues.append("Synthesis process failed")
        
        if score < 0.5:
            recommendations.append("Review expert agent configurations and retry processing")
        
        return QualityMetric(QualityDimension.ACCURACY, max(0.0, score), 0.25, "Synthesis accuracy assessment")
    
    def assess_completeness(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """Assess completeness of synthesis results."""
        from agents.quality_check_interface import QualityMetric, QualityDimension
        
        score = 0.9  # Base score
        issues = []
        recommendations = []
        
        synthesis = agent_result.get("synthesis", {})
        required_fields = ["summary", "insights", "recommendations"]
        
        for field in required_fields:
            if field not in synthesis or not synthesis[field]:
                score -= 0.2
                issues.append(f"Missing or empty {field} in synthesis")
        
        if score < 0.6:
            recommendations.append("Ensure all synthesis components are properly generated")
        
        return QualityMetric(QualityDimension.COMPLETENESS, max(0.0, score), 0.25, "Synthesis completeness assessment")
    
    def assess_relevance(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """Assess relevance of synthesis to original request."""
        from agents.quality_check_interface import QualityMetric, QualityDimension
        
        score = 0.85  # Base score
        issues = []
        recommendations = []
        
        request_type = original_request.get("request_type", "").lower()
        synthesis = agent_result.get("synthesis", {})
        
        # Check if synthesis addresses the request type
        if request_type and synthesis.get("summary"):
            if request_type not in synthesis["summary"].lower():
                score -= 0.2
                issues.append("Synthesis may not directly address the request type")
        
        return QualityMetric(QualityDimension.RELEVANCE, max(0.0, score), 0.2, "Synthesis relevance assessment")
    
    def assess_consistency(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """Assess consistency across expert results."""
        from agents.quality_check_interface import QualityMetric, QualityDimension
        
        score = 0.8  # Base score
        issues = []
        recommendations = []
        
        expert_results = agent_result.get("expert_results", {})
        successful_experts = [r for r in expert_results.values() if "error" not in r]
        
        if len(successful_experts) > 1:
            # Check for consistency in recommendations
            all_recommendations = []
            for result in successful_experts:
                if "recommendations" in result:
                    all_recommendations.extend(result["recommendations"])
            
            if len(set(all_recommendations)) < len(all_recommendations):
                score -= 0.1
                issues.append("Some recommendations may be redundant across experts")
        
        return QualityMetric(QualityDimension.CONSISTENCY, max(0.0, score), 0.15, "Cross-expert consistency assessment")
    
    def assess_clarity(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """Assess clarity of synthesis results."""
        from agents.quality_check_interface import QualityMetric, QualityDimension
        
        score = 0.85  # Base score
        issues = []
        recommendations = []
        
        synthesis = agent_result.get("synthesis", {})
        summary = synthesis.get("summary", "")
        
        if len(summary) < 50:
            score -= 0.2
            issues.append("Synthesis summary may be too brief")
            recommendations.append("Provide more detailed synthesis summary")
        
        return QualityMetric(QualityDimension.CLARITY, max(0.0, score), 0.1, "Synthesis clarity assessment")
    
    def assess_actionability(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """Assess actionability of synthesis results."""
        from agents.quality_check_interface import QualityMetric, QualityDimension
        
        score = 0.8  # Base score
        issues = []
        recommendations = []
        
        synthesis = agent_result.get("synthesis", {})
        recommendations_list = synthesis.get("recommendations", [])
        
        if not recommendations_list:
            score -= 0.3
            issues.append("No actionable recommendations provided")
            recommendations.append("Include specific, actionable recommendations")
        
        return QualityMetric(QualityDimension.ACTIONABILITY, max(0.0, score), 0.05, "Synthesis actionability assessment")
    
    def determine_quality_level(self, overall_score: float) -> str:
        """Determine quality level based on overall score."""
        if overall_score >= 0.9:
            return "EXCELLENT"
        elif overall_score >= 0.8:
            return "VERY_GOOD"
        elif overall_score >= 0.7:
            return "GOOD"
        elif overall_score >= 0.6:
            return "ACCEPTABLE"
        else:
            return "POOR"
    
    def generate_summary(self, metrics: list, overall_score: float) -> str:
        """Generate quality summary for synthesis."""
        if overall_score >= 0.8:
            return "High-quality synthesis with comprehensive expert analysis"
        elif overall_score >= 0.7:
            return "Good quality synthesis meeting publication standards"
        elif overall_score >= 0.6:
            return "Acceptable synthesis with some quality concerns"
        else:
            return "Poor quality synthesis requiring review before publication"
    
    async def _publish_results(self, final_result: Dict[str, Any]):
        """
        Publish results through the file streamer.
        
        Args:
            final_result: Final result to publish
        """
        try:
            # Stream the results
            await self.file_streamer.stream_data(final_result)
            logger.info("Results published successfully through file streamer")
        except Exception as e:
            logger.error(f"Error publishing results: {e}")
            raise

    async def process_request(self, request_data: dict) -> dict:
        """
        Synchronous API wrapper for async process method.
        """
        return await self.process(request_data)

    def get_agents_status(self) -> dict:
        """
        Return the status of all expert agents and the principal agent.
        """
        status = self.get_status()
        return status 