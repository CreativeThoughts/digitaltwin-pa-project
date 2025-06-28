from typing import Dict, Any
from agents.base_agent import BaseExpertAgent
from agents.quality_check_interface import QualityMetric, QualityDimension

class FinancialHealthExpert(BaseExpertAgent):
    """Expert agent specialized in financial health analysis and recommendations."""
    
    def __init__(self, config_list=None):
        system_message = """You are a Financial Health Expert with deep knowledge of:
        - Personal finance management
        - Budget planning and optimization
        - Investment strategies and portfolio management
        - Debt management and reduction
        - Credit score improvement
        - Retirement planning
        - Tax optimization strategies
        - Insurance planning
        - Financial goal setting
        - Risk assessment and management
        
        Your role is to analyze financial-related requests and provide expert advice on:
        1. Financial health assessment
        2. Budget optimization strategies
        3. Investment recommendations
        4. Debt reduction plans
        5. Financial goal achievement
        6. Risk management strategies
        
        Always provide data-driven, actionable recommendations with clear implementation steps.
        Consider both short-term and long-term financial implications in your analysis.
        Ensure recommendations are personalized and realistic for the user's financial situation."""
        
        super().__init__(
            name="FinancialHealthExpert",
            system_message=system_message,
            expertise="financial_health",
            config_list=config_list
        )
    
    async def _expert_process(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process financial health requests with expert knowledge.
        
        Args:
            request_data: Request data dictionary
            
        Returns:
            Dictionary containing financial analysis and recommendations
        """
        description = request_data.get("description", "")
        user_id = request_data.get("user_id", "")
        metadata = request_data.get("metadata", {})
        
        # Analyze the request using the agent
        analysis_prompt = f"""
        Analyze the following financial health request and provide expert recommendations:
        
        User ID: {user_id}
        Request Description: {description}
        Additional Context: {metadata}
        
        Please provide:
        1. Financial health assessment
        2. Key financial issues identified
        3. Budget optimization strategies
        4. Investment recommendations
        5. Debt management strategies
        6. Risk assessment
        7. Implementation timeline
        8. Expected financial outcomes
        
        Format your response as a structured analysis with clear sections.
        """
        
        # Simulate agent processing (in real implementation, this would use AutoGen conversation)
        # For now, we'll create a structured response based on the request
        result = self._generate_financial_analysis(description, metadata)
        
        return result
    
    def _generate_financial_analysis(self, description: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate financial analysis based on request description.
        
        Args:
            description: Request description
            metadata: Additional metadata
            
        Returns:
            Dictionary containing analysis results
        """
        # Analyze keywords in description to determine focus areas
        description_lower = description.lower()
        
        analysis = {
            "analysis_type": "financial_health",
            "financial_health_score": "good",
            "key_issues": [],
            "budget_optimization": [],
            "investment_recommendations": [],
            "debt_management": [],
            "risk_assessment": [],
            "implementation_timeline": "3-12 months",
            "expected_outcomes": [],
            "priority_actions": [],
            "estimated_savings": "10-25%",
            "risk_level": "moderate"
        }
        
        # Budget-related analysis
        if any(word in description_lower for word in ["budget", "spending", "expenses", "cost"]):
            analysis["key_issues"].append("Budget optimization needed")
            analysis["budget_optimization"].append("Implement 50/30/20 budgeting rule")
            analysis["budget_optimization"].append("Track all expenses for 30 days")
            analysis["budget_optimization"].append("Identify and reduce discretionary spending")
            analysis["expected_outcomes"].append("15-25% reduction in unnecessary expenses")
            analysis["priority_actions"].append("Set up expense tracking system")
        
        # Investment-related analysis
        if any(word in description_lower for word in ["investment", "portfolio", "savings", "retirement"]):
            analysis["key_issues"].append("Investment strategy optimization needed")
            analysis["investment_recommendations"].append("Diversify investment portfolio")
            analysis["investment_recommendations"].append("Increase retirement contributions")
            analysis["investment_recommendations"].append("Consider index fund investments")
            analysis["expected_outcomes"].append("8-12% annual investment returns")
            analysis["priority_actions"].append("Review and rebalance investment portfolio")
        
        # Debt-related analysis
        if any(word in description_lower for word in ["debt", "credit", "loan", "payment"]):
            analysis["key_issues"].append("Debt management strategy needed")
            analysis["debt_management"].append("Prioritize high-interest debt repayment")
            analysis["debt_management"].append("Consider debt consolidation options")
            analysis["debt_management"].append("Negotiate lower interest rates")
            analysis["expected_outcomes"].append("20-40% reduction in debt payments")
            analysis["priority_actions"].append("Create debt repayment plan")
        
        # General financial health
        if "financial" in description_lower or "money" in description_lower or "finance" in description_lower:
            analysis["key_issues"].append("Comprehensive financial health improvement needed")
            analysis["budget_optimization"].append("Implement comprehensive financial planning")
            analysis["investment_recommendations"].append("Develop long-term investment strategy")
            analysis["debt_management"].append("Create debt reduction timeline")
            analysis["expected_outcomes"].append("25-35% overall financial improvement")
            analysis["priority_actions"].append("Conduct comprehensive financial audit")
        
        # If no specific areas identified, provide general recommendations
        if not analysis["key_issues"]:
            analysis["key_issues"].append("General financial health assessment needed")
            analysis["budget_optimization"].append("Implement basic budgeting system")
            analysis["investment_recommendations"].append("Start emergency fund savings")
            analysis["debt_management"].append("Review all outstanding debts")
            analysis["expected_outcomes"].append("10-20% overall financial improvement")
            analysis["priority_actions"].append("Schedule financial health assessment")
        
        return analysis
    
    # Quality Assessment Methods
    def assess_accuracy(self, agent_result: Dict[str, Any], original_request: Dict[str, Any]) -> QualityMetric:
        """
        Assess the accuracy of financial health analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Accuracy assessment
        """
        description = original_request.get("description", "").lower()
        analysis = agent_result.get("analysis_type", "")
        
        # Check if analysis type matches request
        if analysis != "financial_health":
            return QualityMetric(
                dimension=QualityDimension.ACCURACY,
                score=0.3,
                weight=0.3,
                description="Analysis type mismatch - not financial health focused",
                issues=["Analysis type does not match financial health expertise"],
                recommendations=["Ensure analysis focuses on financial health aspects"]
            )
        
        # Check for financial-related keywords in response
        financial_keywords = ["budget", "investment", "debt", "savings", "financial", "money", "expense", "income"]
        response_text = str(agent_result).lower()
        keyword_matches = sum(1 for keyword in financial_keywords if keyword in response_text)
        
        if keyword_matches >= 4:
            score = 0.9
            description = f"High accuracy: {keyword_matches} financial concepts identified"
            issues = []
            recommendations = []
        elif keyword_matches >= 2:
            score = 0.7
            description = f"Moderate accuracy: {keyword_matches} financial concepts identified"
            issues = ["Limited financial-specific analysis"]
            recommendations = ["Include more financial-specific recommendations"]
        else:
            score = 0.4
            description = "Low accuracy: No financial-specific analysis detected"
            issues = ["No financial-specific analysis provided"]
            recommendations = ["Focus analysis on financial health aspects"]
        
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
        Assess the completeness of financial health analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Completeness assessment
        """
        required_sections = [
            "key_issues", "budget_optimization", "investment_recommendations", 
            "debt_management", "expected_outcomes", "priority_actions"
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
        Assess the relevance of financial health analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Relevance assessment
        """
        description = original_request.get("description", "").lower()
        request_keywords = ["financial", "money", "budget", "investment", "debt", "savings", "expense", "income"]
        
        # Check if request contains financial-related keywords
        request_relevance = sum(1 for keyword in request_keywords if keyword in description)
        
        if request_relevance >= 2:
            score = 0.9
            description = "Highly relevant: Request clearly financial-focused"
            issues = []
            recommendations = []
        elif request_relevance >= 1:
            score = 0.7
            description = "Moderately relevant: Some financial aspects in request"
            issues = ["Request could be more financial-specific"]
            recommendations = ["Clarify financial-specific requirements"]
        else:
            score = 0.4
            description = "Low relevance: Request not clearly financial-focused"
            issues = ["Request lacks financial-specific context"]
            recommendations = ["Provide more financial-specific context in request"]
        
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
        Assess the consistency of financial health analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Consistency assessment
        """
        # Check for consistency in savings estimates
        estimated_savings = agent_result.get("estimated_savings", "")
        expected_outcomes = agent_result.get("expected_outcomes", [])
        
        # Look for savings percentages in expected outcomes
        savings_mentioned = any("reduction" in outcome.lower() or "%" in outcome for outcome in expected_outcomes)
        
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
        Assess the clarity of financial health analysis.
        
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
        Assess the actionability of financial health analysis.
        
        Args:
            agent_result: The result from the agent
            original_request: The original request
            
        Returns:
            QualityMetric: Actionability assessment
        """
        # Check for actionable recommendations
        budget_optimization = agent_result.get("budget_optimization", [])
        investment_recommendations = agent_result.get("investment_recommendations", [])
        debt_management = agent_result.get("debt_management", [])
        
        total_recommendations = len(budget_optimization) + len(investment_recommendations) + len(debt_management)
        
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
        Get the minimum quality threshold for financial health expert.
        
        Returns:
            float: Minimum acceptable quality score (0.0 to 1.0)
        """
        return 0.75  # Higher threshold for financial advice due to monetary implications 