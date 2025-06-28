from typing import Dict, Any
from agents.base_agent import BaseExpertAgent
from agents.quality_check_interface import QualityMetric, QualityDimension

class VehicleManagementExpert(BaseExpertAgent):
    """Expert agent specialized in vehicle management and optimization."""
    
    def __init__(self, config_list=None):
        system_message = """You are a Vehicle Management Expert with deep knowledge of:
        - Vehicle maintenance and service scheduling
        - Fuel efficiency optimization
        - Vehicle cost analysis and budgeting
        - Insurance and registration management
        - Vehicle safety and compliance
        - Fleet management strategies
        - Electric and hybrid vehicle considerations
        - Vehicle replacement planning
        - Driving behavior optimization
        - Environmental impact reduction
        
        Your role is to analyze vehicle-related requests and provide expert advice on:
        1. Vehicle maintenance optimization
        2. Cost reduction strategies
        3. Safety improvements
        4. Efficiency enhancements
        5. Technology recommendations
        6. Environmental considerations
        
        Always provide actionable, data-driven recommendations with clear implementation steps.
        Consider both immediate needs and long-term vehicle health in your analysis.
        Ensure recommendations are practical and cost-effective for the user's situation."""
        
        super().__init__(
            name="VehicleManagementExpert",
            system_message=system_message,
            expertise="vehicle_management",
            config_list=config_list
        )
    
    async def _expert_process(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process vehicle management requests with expert knowledge.
        
        Args:
            request_data: Request data dictionary
            
        Returns:
            Dictionary containing vehicle analysis and recommendations
        """
        description = request_data.get("description", "")
        user_id = request_data.get("user_id", "")
        metadata = request_data.get("metadata", {})
        
        # Analyze the request using the agent
        analysis_prompt = f"""
        Analyze the following vehicle management request and provide expert recommendations:
        
        User ID: {user_id}
        Request Description: {description}
        Additional Context: {metadata}
        
        Please provide:
        1. Vehicle health assessment
        2. Maintenance recommendations
        3. Cost optimization strategies
        4. Safety improvements
        5. Efficiency enhancements
        6. Implementation timeline
        7. Expected benefits
        8. Risk considerations
        
        Format your response as a structured analysis with clear sections.
        """
        
        # Simulate agent processing (in real implementation, this would use AutoGen conversation)
        # For now, we'll create a structured response based on the request
        result = self._generate_vehicle_analysis(description, metadata)
        
        return result
    
    def _generate_vehicle_analysis(self, description: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate vehicle analysis based on request description.
        
        Args:
            description: Request description
            metadata: Additional metadata
            
        Returns:
            Dictionary containing analysis results
        """
        # Analyze keywords in description to determine focus areas
        description_lower = description.lower()
        
        analysis = {
            "analysis_type": "vehicle_management",
            "vehicle_health_score": "good",
            "key_issues": [],
            "maintenance_recommendations": [],
            "cost_optimization": [],
            "safety_improvements": [],
            "efficiency_enhancements": [],
            "implementation_timeline": "1-6 months",
            "expected_benefits": [],
            "priority_actions": [],
            "estimated_savings": "15-30%",
            "risk_level": "low"
        }
        
        # Maintenance-related analysis
        if any(word in description_lower for word in ["maintenance", "service", "repair", "oil", "tire"]):
            analysis["key_issues"].append("Vehicle maintenance optimization needed")
            analysis["maintenance_recommendations"].append("Implement preventive maintenance schedule")
            analysis["maintenance_recommendations"].append("Regular oil changes and filter replacements")
            analysis["maintenance_recommendations"].append("Tire rotation and alignment checks")
            analysis["expected_benefits"].append("Extended vehicle lifespan and reduced repair costs")
            analysis["priority_actions"].append("Schedule comprehensive vehicle inspection")
        
        # Fuel efficiency analysis
        if any(word in description_lower for word in ["fuel", "gas", "mileage", "efficiency", "consumption"]):
            analysis["key_issues"].append("Fuel efficiency optimization needed")
            analysis["efficiency_enhancements"].append("Optimize driving behavior and routes")
            analysis["efficiency_enhancements"].append("Maintain proper tire pressure")
            analysis["efficiency_enhancements"].append("Reduce vehicle weight and aerodynamic drag")
            analysis["expected_benefits"].append("20-30% improvement in fuel efficiency")
            analysis["priority_actions"].append("Implement fuel tracking and monitoring system")
        
        # Cost-related analysis
        if any(word in description_lower for word in ["cost", "budget", "expense", "insurance", "registration"]):
            analysis["key_issues"].append("Vehicle cost optimization needed")
            analysis["cost_optimization"].append("Shop around for better insurance rates")
            analysis["cost_optimization"].append("Compare fuel prices and use rewards programs")
            analysis["cost_optimization"].append("Consider carpooling or ride-sharing options")
            analysis["expected_benefits"].append("15-25% reduction in vehicle operating costs")
            analysis["priority_actions"].append("Conduct comprehensive cost analysis")
        
        # Safety-related analysis
        if any(word in description_lower for word in ["safety", "brake", "light", "seat", "airbag"]):
            analysis["key_issues"].append("Vehicle safety improvements needed")
            analysis["safety_improvements"].append("Regular brake system inspections")
            analysis["safety_improvements"].append("Ensure all lights and signals work properly")
            analysis["safety_improvements"].append("Check seat belts and airbag systems")
            analysis["expected_benefits"].append("Enhanced vehicle and passenger safety")
            analysis["priority_actions"].append("Schedule safety inspection and repairs")
        
        # General vehicle management
        if "vehicle" in description_lower or "car" in description_lower or "auto" in description_lower:
            analysis["key_issues"].append("Comprehensive vehicle management optimization needed")
            analysis["maintenance_recommendations"].append("Implement comprehensive maintenance program")
            analysis["cost_optimization"].append("Develop vehicle cost management strategy")
            analysis["safety_improvements"].append("Establish regular safety check protocols")
            analysis["expected_benefits"].append("25-35% overall vehicle cost and efficiency improvement")
            analysis["priority_actions"].append("Create comprehensive vehicle management plan")
        
        # If no specific areas identified, provide general recommendations
        if not analysis["key_issues"]:
            analysis["key_issues"].append("General vehicle management assessment needed")
            analysis["maintenance_recommendations"].append("Establish regular maintenance schedule")
            analysis["cost_optimization"].append("Track all vehicle-related expenses")
            analysis["safety_improvements"].append("Schedule regular safety inspections")
            analysis["expected_benefits"].append("10-20% overall vehicle improvement")
            analysis["priority_actions"].append("Schedule comprehensive vehicle assessment")
        
        return analysis
    
    # Quality Assessment Methods
    def assess_accuracy(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the accuracy of vehicle management analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Accuracy assessment
        """
        description = original_request.get("description", "").lower()
        analysis = agent_result.get("analysis_type", "")
        
        # Check if analysis type matches request
        if analysis != "vehicle_management":
            return QualityMetric(
                dimension=QualityDimension.ACCURACY,
                score=0.3,
                weight=0.3,
                description="Analysis type mismatch - not vehicle management focused",
                issues=["Analysis type does not match vehicle management expertise"],
                recommendations=["Ensure analysis focuses on vehicle management aspects"]
            )
        
        # Check for vehicle-related keywords in response
        vehicle_keywords = ["maintenance", "fuel", "safety", "cost", "vehicle", "car", "tire", "oil", "brake"]
        response_text = str(agent_result).lower()
        keyword_matches = sum(1 for keyword in vehicle_keywords if keyword in response_text)
        
        if keyword_matches >= 4:
            score = 0.9
            description = f"High accuracy: {keyword_matches} vehicle-related concepts identified"
            issues = []
            recommendations = []
        elif keyword_matches >= 2:
            score = 0.7
            description = f"Moderate accuracy: {keyword_matches} vehicle-related concepts identified"
            issues = ["Limited vehicle-specific analysis"]
            recommendations = ["Include more vehicle-specific recommendations"]
        else:
            score = 0.4
            description = "Low accuracy: No vehicle-specific analysis detected"
            issues = ["No vehicle-specific analysis provided"]
            recommendations = ["Focus analysis on vehicle management aspects"]
        
        return QualityMetric(
            dimension=QualityDimension.ACCURACY,
            score=score,
            weight=0.3,
            description=description,
            issues=issues,
            recommendations=recommendations
        )
    
    def assess_completeness(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the completeness of vehicle management analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Completeness assessment
        """
        required_sections = [
            "key_issues", "maintenance_recommendations", "cost_optimization", 
            "safety_improvements", "expected_benefits", "priority_actions"
        ]
        
        missing_sections = []
        present_sections = []
        
        for section in required_sections:
            if section in agent_result and agent_result[section]:
                present_sections.append(section)
            else:
                missing_sections.append(section)
        
        if len(missing_sections) == 0:
            score = 1.0
            description = "Complete analysis: All required sections present"
            issues = []
            recommendations = []
        elif len(missing_sections) <= 2:
            score = 0.8
            description = f"Mostly complete: Missing {len(missing_sections)} sections"
            issues = [f"Missing sections: {', '.join(missing_sections)}"]
            recommendations = [f"Add missing sections: {', '.join(missing_sections)}"]
        else:
            score = 0.5
            description = f"Incomplete analysis: Missing {len(missing_sections)} sections"
            issues = [f"Multiple missing sections: {', '.join(missing_sections)}"]
            recommendations = ["Complete all required analysis sections"]
        
        return QualityMetric(
            dimension=QualityDimension.COMPLETENESS,
            score=score,
            weight=0.2,
            description=description,
            issues=issues,
            recommendations=recommendations
        )
    
    def assess_relevance(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the relevance of vehicle management analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Relevance assessment
        """
        description = original_request.get("description", "").lower()
        request_keywords = ["vehicle", "car", "auto", "maintenance", "fuel", "safety", "cost", "tire", "oil"]
        
        # Check if request contains vehicle-related keywords
        request_relevance = sum(1 for keyword in request_keywords if keyword in description)
        
        if request_relevance >= 2:
            score = 0.9
            description = "Highly relevant: Request clearly vehicle-focused"
            issues = []
            recommendations = []
        elif request_relevance >= 1:
            score = 0.7
            description = "Moderately relevant: Some vehicle aspects in request"
            issues = ["Request could be more vehicle-specific"]
            recommendations = ["Clarify vehicle-specific requirements"]
        else:
            score = 0.4
            description = "Low relevance: Request not clearly vehicle-focused"
            issues = ["Request lacks vehicle-specific context"]
            recommendations = ["Provide more vehicle-specific context in request"]
        
        return QualityMetric(
            dimension=QualityDimension.RELEVANCE,
            score=score,
            weight=0.2,
            description=description,
            issues=issues,
            recommendations=recommendations
        )
    
    def assess_consistency(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the consistency of vehicle management analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Consistency assessment
        """
        # Check for consistency in savings estimates
        estimated_savings = agent_result.get("estimated_savings", "")
        expected_benefits = agent_result.get("expected_benefits", [])
        
        # Look for savings percentages in expected benefits
        savings_mentioned = any("reduction" in benefit.lower() or "%" in benefit for benefit in expected_benefits)
        
        if estimated_savings and savings_mentioned:
            score = 0.9
            description = "Consistent savings estimates across analysis"
            issues = []
            recommendations = []
        elif estimated_savings or savings_mentioned:
            score = 0.7
            description = "Partial savings consistency"
            issues = ["Savings estimates not consistently mentioned"]
            recommendations = ["Ensure savings estimates are consistent throughout"]
        else:
            score = 0.5
            description = "No consistent savings estimates found"
            issues = ["No savings estimates provided"]
            recommendations = ["Include consistent savings estimates"]
        
        return QualityMetric(
            dimension=QualityDimension.CONSISTENCY,
            score=score,
            weight=0.1,
            description=description,
            issues=issues,
            recommendations=recommendations
        )
    
    def assess_clarity(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the clarity of vehicle management analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Clarity assessment
        """
        # Check for clear priority actions
        priority_actions = agent_result.get("priority_actions", [])
        implementation_timeline = agent_result.get("implementation_timeline", "")
        
        if len(priority_actions) >= 2 and implementation_timeline:
            score = 0.9
            description = "Clear priority actions and timeline provided"
            issues = []
            recommendations = []
        elif len(priority_actions) >= 1:
            score = 0.7
            description = "Some priority actions provided"
            issues = ["Limited implementation guidance"]
            recommendations = ["Provide more detailed priority actions and timeline"]
        else:
            score = 0.4
            description = "No clear priority actions"
            issues = ["No implementation guidance provided"]
            recommendations = ["Include clear priority actions and timeline"]
        
        return QualityMetric(
            dimension=QualityDimension.CLARITY,
            score=score,
            weight=0.05,
            description=description,
            issues=issues,
            recommendations=recommendations
        )
    
    def assess_actionability(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the actionability of vehicle management analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Actionability assessment
        """
        # Check for actionable recommendations
        maintenance_recommendations = agent_result.get("maintenance_recommendations", [])
        cost_optimization = agent_result.get("cost_optimization", [])
        safety_improvements = agent_result.get("safety_improvements", [])
        
        total_recommendations = len(maintenance_recommendations) + len(cost_optimization) + len(safety_improvements)
        
        if total_recommendations >= 4:
            score = 0.9
            description = f"Highly actionable: {total_recommendations} specific recommendations"
            issues = []
            recommendations = []
        elif total_recommendations >= 2:
            score = 0.7
            description = f"Somewhat actionable: {total_recommendations} recommendations"
            issues = ["Limited actionable recommendations"]
            recommendations = ["Provide more specific actionable recommendations"]
        else:
            score = 0.4
            description = "Not actionable: No specific recommendations"
            issues = ["No actionable recommendations provided"]
            recommendations = ["Include specific actionable recommendations"]
        
        return QualityMetric(
            dimension=QualityDimension.ACTIONABILITY,
            score=score,
            weight=0.05,
            description=description,
            issues=issues,
            recommendations=recommendations
        )
    
    def get_quality_threshold(self) -> float:
        """
        Get the minimum quality threshold for vehicle management expert.
        
        Returns:
            float: Minimum acceptable quality score (0.0 to 1.0)
        """
        return 0.65  # Standard threshold for vehicle management 