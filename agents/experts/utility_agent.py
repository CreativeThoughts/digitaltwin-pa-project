from typing import Dict, Any
from agents.base_agent import BaseExpertAgent
from agents.quality_check_interface import QualityMetric, QualityDimension

class UtilityManagementExpert(BaseExpertAgent):
    """Expert agent specialized in utility management and optimization."""
    
    def __init__(self, config_list=None):
        system_message = """You are a Utility Management Expert with deep knowledge of:
        - Energy consumption optimization
        - Water usage management
        - Waste management strategies
        - Utility cost analysis and reduction
        - Smart home integration for utilities
        - Renewable energy solutions
        - Utility bill analysis and optimization
        - Energy efficiency recommendations
        - Utility infrastructure planning
        - Sustainability practices
        
        Your role is to analyze utility-related requests and provide expert advice on:
        1. Identifying optimization opportunities
        2. Cost reduction strategies
        3. Efficiency improvements
        4. Technology recommendations
        5. Sustainability measures
        
        Always provide actionable, data-driven recommendations with clear implementation steps.
        Consider both short-term and long-term benefits in your analysis."""
        
        super().__init__(
            name="UtilityManagementExpert",
            system_message=system_message,
            expertise="utility_management",
            config_list=config_list
        )
    
    async def _expert_process(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process utility management requests with expert knowledge.
        
        Args:
            request_data: Request data dictionary
            
        Returns:
            Dictionary containing utility analysis and recommendations
        """
        description = request_data.get("description", "")
        user_id = request_data.get("user_id", "")
        metadata = request_data.get("metadata", {})
        
        # Analyze the request using the agent
        analysis_prompt = f"""
        Analyze the following utility management request and provide expert recommendations:
        
        User ID: {user_id}
        Request Description: {description}
        Additional Context: {metadata}
        
        Please provide:
        1. Key issues identified
        2. Optimization opportunities
        3. Cost-saving recommendations
        4. Implementation steps
        5. Expected benefits
        6. Risk considerations
        7. Technology recommendations (if applicable)
        
        Format your response as a structured analysis with clear sections.
        """
        
        # Simulate agent processing (in real implementation, this would use AutoGen conversation)
        # For now, we'll create a structured response based on the request
        result = self._generate_utility_analysis(description, metadata)
        
        return result
    
    def _generate_utility_analysis(self, description: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate utility analysis based on request description.
        
        Args:
            description: Request description
            metadata: Additional metadata
            
        Returns:
            Dictionary containing analysis results
        """
        # Analyze keywords in description to determine focus areas
        description_lower = description.lower()
        
        analysis = {
            "analysis_type": "utility_management",
            "key_issues": [],
            "optimization_opportunities": [],
            "cost_savings_recommendations": [],
            "implementation_steps": [],
            "expected_benefits": [],
            "risk_considerations": [],
            "technology_recommendations": [],
            "priority_level": "medium",
            "estimated_savings": "5-15%",
            "implementation_timeline": "3-6 months"
        }
        
        # Energy-related analysis
        if any(word in description_lower for word in ["energy", "electricity", "power", "consumption"]):
            analysis["key_issues"].append("High energy consumption patterns detected")
            analysis["optimization_opportunities"].append("Implement smart energy monitoring systems")
            analysis["cost_savings_recommendations"].append("Switch to energy-efficient appliances")
            analysis["implementation_steps"].append("Conduct energy audit and identify high-consumption areas")
            analysis["expected_benefits"].append("15-25% reduction in energy costs")
            analysis["technology_recommendations"].append("Smart meters and energy monitoring devices")
        
        # Water-related analysis
        if any(word in description_lower for word in ["water", "usage", "bills", "leak"]):
            analysis["key_issues"].append("Water usage optimization needed")
            analysis["optimization_opportunities"].append("Install water-efficient fixtures")
            analysis["cost_savings_recommendations"].append("Implement leak detection systems")
            analysis["implementation_steps"].append("Audit water usage patterns and identify leaks")
            analysis["expected_benefits"].append("10-20% reduction in water costs")
            analysis["technology_recommendations"].append("Smart water meters and leak detectors")
        
        # General utility optimization
        if "optimization" in description_lower or "efficiency" in description_lower:
            analysis["key_issues"].append("Overall utility efficiency improvement needed")
            analysis["optimization_opportunities"].append("Implement comprehensive utility monitoring")
            analysis["cost_savings_recommendations"].append("Bundle utility services for better rates")
            analysis["implementation_steps"].append("Develop utility management strategy and timeline")
            analysis["expected_benefits"].append("20-30% overall utility cost reduction")
            analysis["technology_recommendations"].append("Integrated utility management platform")
        
        # If no specific areas identified, provide general recommendations
        if not analysis["key_issues"]:
            analysis["key_issues"].append("General utility management improvement opportunity")
            analysis["optimization_opportunities"].append("Implement comprehensive utility monitoring and optimization")
            analysis["cost_savings_recommendations"].append("Audit all utility services for optimization opportunities")
            analysis["implementation_steps"].append("Conduct comprehensive utility audit and develop optimization plan")
            analysis["expected_benefits"].append("10-25% overall utility cost reduction")
            analysis["technology_recommendations"].append("Smart utility monitoring and management systems")
        
        return analysis
    
    # Quality Assessment Methods
    def assess_accuracy(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the accuracy of utility management analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Accuracy assessment
        """
        description = original_request.get("description", "").lower()
        analysis = agent_result.get("analysis_type", "")
        
        # Check if analysis type matches request
        if analysis != "utility_management":
            return QualityMetric(
                dimension=QualityDimension.ACCURACY,
                score=0.3,
                weight=0.3,
                description="Analysis type mismatch - not utility management focused",
                issues=["Analysis type does not match utility management expertise"],
                recommendations=["Ensure analysis focuses on utility management aspects"]
            )
        
        # Check for utility-related keywords in response
        utility_keywords = ["energy", "water", "electricity", "gas", "utility", "consumption", "efficiency"]
        response_text = str(agent_result).lower()
        keyword_matches = sum(1 for keyword in utility_keywords if keyword in response_text)
        
        if keyword_matches >= 3:
            score = 0.9
            description = f"High accuracy: {keyword_matches} utility-related concepts identified"
            issues = []
            recommendations = []
        elif keyword_matches >= 1:
            score = 0.7
            description = f"Moderate accuracy: {keyword_matches} utility-related concepts identified"
            issues = ["Limited utility-specific analysis"]
            recommendations = ["Include more utility-specific recommendations"]
        else:
            score = 0.4
            description = "Low accuracy: No utility-specific analysis detected"
            issues = ["No utility-specific analysis provided"]
            recommendations = ["Focus analysis on utility management aspects"]
        
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
        Assess the completeness of utility management analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Completeness assessment
        """
        required_sections = [
            "key_issues", "optimization_opportunities", "cost_savings_recommendations",
            "implementation_steps", "expected_benefits"
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
        Assess the relevance of utility management analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Relevance assessment
        """
        description = original_request.get("description", "").lower()
        request_keywords = ["utility", "energy", "water", "electricity", "gas", "bills", "consumption"]
        
        # Check if request contains utility-related keywords
        request_relevance = sum(1 for keyword in request_keywords if keyword in description)
        
        if request_relevance >= 2:
            score = 0.9
            description = "Highly relevant: Request clearly utility-focused"
            issues = []
            recommendations = []
        elif request_relevance >= 1:
            score = 0.7
            description = "Moderately relevant: Some utility aspects in request"
            issues = ["Request could be more utility-specific"]
            recommendations = ["Clarify utility-specific requirements"]
        else:
            score = 0.4
            description = "Low relevance: Request not clearly utility-focused"
            issues = ["Request lacks utility-specific context"]
            recommendations = ["Provide more utility-specific context in request"]
        
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
        Assess the consistency of utility management analysis.
        
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
        Assess the clarity of utility management analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Clarity assessment
        """
        # Check for clear implementation steps
        implementation_steps = agent_result.get("implementation_steps", [])
        
        if len(implementation_steps) >= 3:
            score = 0.9
            description = "Clear implementation steps provided"
            issues = []
            recommendations = []
        elif len(implementation_steps) >= 1:
            score = 0.7
            description = "Some implementation steps provided"
            issues = ["Limited implementation guidance"]
            recommendations = ["Provide more detailed implementation steps"]
        else:
            score = 0.4
            description = "No clear implementation steps"
            issues = ["No implementation guidance provided"]
            recommendations = ["Include clear implementation steps"]
        
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
        Assess the actionability of utility management analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Actionability assessment
        """
        # Check for actionable recommendations
        cost_savings_recommendations = agent_result.get("cost_savings_recommendations", [])
        technology_recommendations = agent_result.get("technology_recommendations", [])
        
        total_recommendations = len(cost_savings_recommendations) + len(technology_recommendations)
        
        if total_recommendations >= 3:
            score = 0.9
            description = f"Highly actionable: {total_recommendations} specific recommendations"
            issues = []
            recommendations = []
        elif total_recommendations >= 1:
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
        Get the minimum quality threshold for utility management expert.
        
        Returns:
            float: Minimum acceptable quality score (0.0 to 1.0)
        """
        return 0.7  # Higher threshold for utility management due to cost implications 