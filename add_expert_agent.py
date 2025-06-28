#!/usr/bin/env python3
"""
Utility script to add new expert agents to the Agentic AI Solution.
This script helps create the necessary files and update the principal agent.
"""

import os
import re
from pathlib import Path

def create_expert_agent_template(expert_name: str, expertise: str, description: str):
    """
    Create a new expert agent template.
    
    Args:
        expert_name: Name of the expert agent (e.g., "HomeSecurityExpert")
        expertise: Expertise area (e.g., "home_security")
        description: Brief description of the expert's capabilities
    """
    
    # Convert to snake_case for file names
    file_name = re.sub(r'(?<!^)(?=[A-Z])', '_', expert_name).lower()
    
    # Create the expert agent file
    expert_file_content = f'''from typing import Dict, Any
from agents.base_agent import BaseExpertAgent

class {expert_name}(BaseExpertAgent):
    """Expert agent specialized in {description}."""
    
    def __init__(self, config_list=None):
        system_message = """You are a {expert_name} with deep knowledge of:
        - [Add specific areas of expertise]
        - [Add more areas of expertise]
        - [Add more areas of expertise]
        
        Your role is to analyze {expertise} requests and provide expert advice on:
        1. [Add specific responsibilities]
        2. [Add more responsibilities]
        3. [Add more responsibilities]
        
        Always provide actionable, data-driven recommendations with clear implementation steps.
        Consider both short-term and long-term benefits in your analysis."""
        
        super().__init__(
            name="{expert_name}",
            system_message=system_message,
            expertise="{expertise}",
            config_list=config_list
        )
    
    async def _expert_process(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process {expertise} requests with expert knowledge.
        
        Args:
            request_data: Request data dictionary
            
        Returns:
            Dictionary containing {expertise} analysis and recommendations
        """
        description = request_data.get("description", "")
        user_id = request_data.get("user_id", "")
        metadata = request_data.get("metadata", {{}})
        
        # Simulate agent processing (in real implementation, this would use AutoGen conversation)
        # For now, we'll create a structured response based on the request
        result = self._generate_{expertise}_analysis(description, metadata)
        
        return result
    
    def _generate_{expertise}_analysis(self, description: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate {expertise} analysis based on request description.
        
        Args:
            description: Request description
            metadata: Additional metadata
            
        Returns:
            Dictionary containing analysis results
        """
        # Analyze keywords in description to determine focus areas
        description_lower = description.lower()
        
        analysis = {{
            "analysis_type": "{expertise}",
            "key_issues": [],
            "recommendations": [],
            "implementation_steps": [],
            "expected_benefits": [],
            "priority_actions": [],
            "timeline": "3-6 months",
            "estimated_improvement": "10-25%"
        }}
        
        # Add your specific analysis logic here
        # Example:
        # if "keyword" in description_lower:
        #     analysis["key_issues"].append("Issue identified")
        #     analysis["recommendations"].append("Recommendation")
        
        # If no specific areas identified, provide general recommendations
        if not analysis["key_issues"]:
            analysis["key_issues"].append("General {expertise} improvement opportunity")
            analysis["recommendations"].append("Implement comprehensive {expertise} strategy")
            analysis["implementation_steps"].append("Conduct {expertise} assessment and develop improvement plan")
            analysis["expected_benefits"].append("Improved {expertise} and cost savings")
            analysis["priority_actions"].append("Develop {expertise} improvement plan")
        
        return analysis
'''
    
    # Write the expert agent file
    expert_file_path = Path(f"agents/experts/{file_name}.py")
    with open(expert_file_path, 'w') as f:
        f.write(expert_file_content)
    
    print(f"Created expert agent file: {expert_file_path}")
    
    # Update the principal agent imports
    update_principal_agent_imports(expert_name, file_name)
    
    # Update the principal agent initialization
    update_principal_agent_initialization(expert_name, expertise)
    
    # Update the principal agent routing
    update_principal_agent_routing(expertise)
    
    print(f"Expert agent '{expert_name}' has been successfully added!")
    print(f"Expertise area: {expertise}")
    print(f"File created: {expert_file_path}")
    print("\nNext steps:")
    print("1. Customize the system_message in the expert agent")
    print("2. Implement specific analysis logic in _generate_{expertise}_analysis method")
    print("3. Add relevant keywords to the principal agent's _analyze_content_for_agents method")
    print("4. Test the new expert agent")

def update_principal_agent_imports(expert_name: str, file_name: str):
    """Update the principal agent imports to include the new expert agent."""
    principal_agent_path = Path("agents/principal_agent.py")
    
    with open(principal_agent_path, 'r') as f:
        content = f.read()
    
    # Add import statement
    import_line = f"from agents.experts.{file_name} import {expert_name}"
    
    # Find the existing imports section and add the new import
    import_section = "from agents.experts.utility_agent import UtilityManagementExpert"
    new_import_section = f"{import_section}\nfrom agents.experts.{file_name} import {expert_name}"
    
    content = content.replace(import_section, new_import_section)
    
    with open(principal_agent_path, 'w') as f:
        f.write(content)
    
    print(f"Updated principal agent imports")

def update_principal_agent_initialization(expert_name: str, expertise: str):
    """Update the principal agent initialization to include the new expert agent."""
    principal_agent_path = Path("agents/principal_agent.py")
    
    with open(principal_agent_path, 'r') as f:
        content = f.read()
    
    # Add expert agent initialization
    init_section = 'self.expert_agents["vehicle_management"] = VehicleManagementExpert('
    new_init_section = f'''self.expert_agents["vehicle_management"] = VehicleManagementExpert(
                config_list=self.config_list
            )
            self.expert_agents["{expertise}"] = {expert_name}('''
    
    content = content.replace(init_section, new_init_section)
    
    with open(principal_agent_path, 'w') as f:
        f.write(content)
    
    print(f"Updated principal agent initialization")

def update_principal_agent_routing(expertise: str):
    """Update the principal agent routing to include the new expertise area."""
    principal_agent_path = Path("agents/principal_agent.py")
    
    with open(principal_agent_path, 'r') as f:
        content = f.read()
    
    # Add to type mapping
    type_mapping_section = '"vehicle_management": ["vehicle_management"],'
    new_type_mapping_section = f'''"vehicle_management": ["vehicle_management"],
            "{expertise}": ["{expertise}"],'''
    
    content = content.replace(type_mapping_section, new_type_mapping_section)
    
    with open(principal_agent_path, 'w') as f:
        f.write(content)
    
    print(f"Updated principal agent routing")

def main():
    """Main function to add a new expert agent."""
    print("=" * 60)
    print("AGENTIC AI SOLUTION - ADD EXPERT AGENT")
    print("=" * 60)
    print()
    
    # Get user input
    expert_name = input("Enter the expert agent name (e.g., HomeSecurityExpert): ").strip()
    if not expert_name:
        print("Expert name is required!")
        return
    
    expertise = input("Enter the expertise area (e.g., home_security): ").strip()
    if not expertise:
        print("Expertise area is required!")
        return
    
    description = input("Enter a brief description of the expert's capabilities: ").strip()
    if not description:
        description = f"{expertise} management and optimization"
    
    # Confirm
    print(f"\nExpert Agent Details:")
    print(f"Name: {expert_name}")
    print(f"Expertise: {expertise}")
    print(f"Description: {description}")
    
    confirm = input("\nProceed with creating this expert agent? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Operation cancelled.")
        return
    
    # Create the expert agent
    try:
        create_expert_agent_template(expert_name, expertise, description)
        print("\nExpert agent created successfully!")
    except Exception as e:
        print(f"Error creating expert agent: {e}")

if __name__ == "__main__":
    main() 