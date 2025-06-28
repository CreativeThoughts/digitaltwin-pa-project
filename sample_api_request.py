#!/usr/bin/env python3
"""
Sample API request script to demonstrate the Quality Check (QC) flow via FastAPI.
This script shows how to make requests to the API and what the response looks like.
"""

import asyncio
import aiohttp
import json
from datetime import datetime

async def test_api_qc_flow():
    """Test the API quality check flow with sample requests."""
    
    # API endpoint (adjust if your server runs on different port)
    base_url = "http://localhost:8000"
    
    print("🚀 API Quality Check Flow Test")
    print("=" * 50)
    
    # Sample request data
    sample_requests = [
        {
            "name": "Utility Management Request",
            "data": {
                "request_id": f"api_utility_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "user_id": "api_user_001",
                "request_type": "utility_management",
                "description": "I need help optimizing my energy consumption and reducing utility bills. My electricity usage has been high and I want to implement energy efficiency measures.",
                "metadata": {
                    "current_energy_bill": "$200/month",
                    "property_type": "residential",
                    "location": "California"
                }
            }
        },
        {
            "name": "Financial Health Request", 
            "data": {
                "request_id": f"api_financial_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "user_id": "api_user_002",
                "request_type": "financial_health",
                "description": "I need financial advice to improve my budget, reduce debt, and start investing. I have credit card debt and want to build savings.",
                "metadata": {
                    "monthly_income": "$5000",
                    "current_debt": "$15000",
                    "savings": "$2000"
                }
            }
        },
        {
            "name": "Multi-Domain Request",
            "data": {
                "request_id": f"api_multi_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "user_id": "api_user_003", 
                "request_type": "comprehensive_analysis",
                "description": "I need comprehensive analysis covering utility optimization, financial planning, and vehicle management. I want to reduce all my expenses and improve efficiency across all areas.",
                "metadata": {
                    "property_type": "residential",
                    "monthly_income": "$6000",
                    "vehicle_count": 2,
                    "current_expenses": "$4000/month"
                }
            }
        }
    ]
    
    async with aiohttp.ClientSession() as session:
        for request_info in sample_requests:
            print(f"\n📊 Testing: {request_info['name']}")
            print("-" * 40)
            
            try:
                # Make API request
                async with session.post(
                    f"{base_url}/process",
                    json=request_info['data'],
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        print_api_qc_results(request_info['name'], result)
                    else:
                        error_text = await response.text()
                        print(f"❌ API Error ({response.status}): {error_text}")
                        
            except Exception as e:
                print(f"❌ Request failed: {e}")

def print_api_qc_results(test_name: str, result: dict):
    """Print API quality check results in a formatted way."""
    
    print(f"✅ {test_name} - API Response:")
    print(f"   Request ID: {result.get('request_id', 'N/A')}")
    print(f"   Processing Time: {result.get('processing_time', 0):.2f}s")
    print(f"   Principal Agent: {result.get('principal_agent', 'N/A')}")
    print(f"   Publication Status: {result.get('publication_status', 'N/A')}")
    print(f"   Approved for Publication: {result.get('approved_for_publication', False)}")
    
    # Print expert results and their QC scores
    expert_results = result.get('expert_results', {})
    print(f"\n   Expert Agents Used: {len(expert_results)}")
    
    for expert_name, expert_result in expert_results.items():
        quality_report = expert_result.get('quality_report', {})
        print(f"\n   🔍 {expert_name.replace('_', ' ').title()}:")
        print(f"      Quality Score: {quality_report.get('overall_score', 0):.2f}")
        print(f"      Quality Level: {quality_report.get('quality_level', 'N/A')}")
        print(f"      Passed Threshold: {quality_report.get('passed_threshold', False)}")
        print(f"      Issues Found: {quality_report.get('total_issues', 0)}")
        print(f"      Recommendations: {quality_report.get('total_recommendations', 0)}")
    
    # Print final synthesis QC
    final_qc = result.get('final_quality_report', {})
    print(f"\n   🎯 Final Synthesis Quality:")
    print(f"      Overall Score: {final_qc.get('overall_score', 0):.2f}")
    print(f"      Quality Level: {final_qc.get('quality_level', 'N/A')}")
    print(f"      Passed Threshold: {final_qc.get('passed_threshold', False)}")
    print(f"      Approved for Publication: {final_qc.get('approved_for_publication', False)}")
    
    # Print synthesis summary
    synthesis = result.get('synthesis', {})
    if synthesis:
        print(f"\n   📊 Synthesis Summary:")
        print(f"      Key Recommendations: {len(synthesis.get('key_recommendations', []))}")
        print(f"      Priority Actions: {len(synthesis.get('priority_actions', []))}")
        print(f"      Expected Benefits: {len(synthesis.get('expected_benefits', []))}")
        print(f"      Implementation Timeline: {synthesis.get('implementation_timeline', 'N/A')}")

def print_sample_request():
    """Print a sample request structure for reference."""
    
    sample_request = {
        "request_id": "sample_request_001",
        "user_id": "user_123",
        "request_type": "utility_management",
        "description": "I need help optimizing my energy consumption and reducing utility bills.",
        "metadata": {
            "current_energy_bill": "$200/month",
            "property_type": "residential",
            "location": "California"
        }
    }
    
    print("\n📝 Sample API Request Structure:")
    print("=" * 40)
    print(json.dumps(sample_request, indent=2))

def print_sample_response():
    """Print a sample response structure for reference."""
    
    sample_response = {
        "request_id": "sample_request_001",
        "processing_time": 2.45,
        "principal_agent": "PrincipalAgent",
        "expert_results": {
            "utility_management": {
                "analysis_type": "utility_management",
                "key_issues": ["High energy consumption patterns detected"],
                "optimization_opportunities": ["Implement smart energy monitoring systems"],
                "cost_savings_recommendations": ["Switch to energy-efficient appliances"],
                "implementation_steps": ["Conduct energy audit and identify high-consumption areas"],
                "expected_benefits": ["15-25% reduction in energy costs"],
                "technology_recommendations": ["Smart meters and energy monitoring devices"],
                "quality_report": {
                    "agent_name": "UtilityManagementExpert",
                    "request_id": "sample_request_001",
                    "overall_score": 0.85,
                    "quality_level": "good",
                    "metrics": [
                        {
                            "dimension": "accuracy",
                            "score": 0.9,
                            "weight": 0.3,
                            "description": "High accuracy: 4 utility-related concepts identified",
                            "issues": [],
                            "recommendations": []
                        }
                    ],
                    "summary": "Quality Assessment: GOOD (Score: 0.85)\nTotal Issues Found: 0\nTotal Recommendations: 0\nNo quality issues detected. Results are ready for publication.",
                    "timestamp": "2024-01-15T10:30:00",
                    "passed_threshold": True,
                    "approved_for_publication": True,
                    "total_issues": 0,
                    "total_recommendations": 0
                }
            }
        },
        "quality_assessments": {
            "utility_management": {
                "agent_name": "UtilityManagementExpert",
                "request_id": "sample_request_001",
                "overall_score": 0.85,
                "quality_level": "good",
                "metrics": [],
                "summary": "Quality Assessment: GOOD (Score: 0.85)",
                "timestamp": "2024-01-15T10:30:00",
                "passed_threshold": True,
                "approved_for_publication": True,
                "total_issues": 0,
                "total_recommendations": 0
            }
        },
        "synthesis": {
            "analysis_type": "comprehensive_multi_domain",
            "overall_quality_score": 0.85,
            "key_recommendations": ["Switch to energy-efficient appliances"],
            "priority_actions": ["Schedule comprehensive vehicle inspection"],
            "expected_benefits": ["15-25% reduction in energy costs"],
            "implementation_timeline": "3-12 months",
            "risk_assessment": "moderate"
        },
        "final_quality_report": {
            "agent_name": "PrincipalAgent",
            "request_id": "sample_request_001",
            "overall_score": 0.82,
            "quality_level": "good",
            "metrics": [],
            "summary": "Quality Assessment: GOOD (Score: 0.82)",
            "timestamp": "2024-01-15T10:30:00",
            "passed_threshold": True,
            "approved_for_publication": True,
            "total_issues": 0,
            "total_recommendations": 0
        },
        "approved_for_publication": True,
        "publication_status": "approved"
    }
    
    print("\n📋 Sample API Response Structure:")
    print("=" * 40)
    print(json.dumps(sample_response, indent=2))

async def main():
    """Main function to run the API test."""
    try:
        # Print sample structures first
        print_sample_request()
        print_sample_response()
        
        # Run API tests
        await test_api_qc_flow()
        
        print("\n✅ API Quality Check Flow Test Completed")
        print("\n💡 To run this test:")
        print("   1. Start your FastAPI server: uvicorn api.routes:app --reload")
        print("   2. Run this script: python sample_api_request.py")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 