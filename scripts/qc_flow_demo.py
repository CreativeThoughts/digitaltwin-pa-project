#!/usr/bin/env python3
"""
Test script to demonstrate the Quality Check (QC) flow.
This script sends sample requests to test different expert agents and shows QC reports.
"""

import asyncio
import json
from datetime import datetime
from agents.principal_agent import PrincipalAgent
from utils.logger import logger

async def test_qc_flow():
    """Test the quality check flow with different types of requests."""
    
    # Initialize the principal agent
    principal_agent = PrincipalAgent()
    await principal_agent.initialize()
    
    print("🚀 Quality Check Flow Test Started")
    print("=" * 60)
    
    # Test Case 1: Utility Management Request
    print("\n📊 Test Case 1: Utility Management Request")
    print("-" * 40)
    
    utility_request = {
        "request_id": f"utility_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "user_id": "user_001",
        "request_type": "utility_management",
        "description": "I need help optimizing my energy consumption and reducing utility bills. My electricity usage has been high and I want to implement energy efficiency measures.",
        "metadata": {
            "current_energy_bill": "$200/month",
            "property_type": "residential",
            "location": "California"
        }
    }
    
    try:
        result = await principal_agent.process(utility_request)
        print_qc_results("Utility Management", result)
    except Exception as e:
        print(f"❌ Error in utility test: {e}")
    
    # Test Case 2: Financial Health Request
    print("\n💰 Test Case 2: Financial Health Request")
    print("-" * 40)
    
    financial_request = {
        "request_id": f"financial_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "user_id": "user_002",
        "request_type": "financial_health",
        "description": "I need financial advice to improve my budget, reduce debt, and start investing. I have credit card debt and want to build savings.",
        "metadata": {
            "monthly_income": "$5000",
            "current_debt": "$15000",
            "savings": "$2000"
        }
    }
    
    try:
        result = await principal_agent.process(financial_request)
        print_qc_results("Financial Health", result)
    except Exception as e:
        print(f"❌ Error in financial test: {e}")
    
    # Test Case 3: Vehicle Management Request
    print("\n🚗 Test Case 3: Vehicle Management Request")
    print("-" * 40)
    
    vehicle_request = {
        "request_id": f"vehicle_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "user_id": "user_003",
        "request_type": "vehicle_management",
        "description": "I need help with vehicle maintenance optimization and fuel efficiency. My car is consuming too much fuel and I want to reduce costs.",
        "metadata": {
            "vehicle_type": "sedan",
            "fuel_consumption": "25 mpg",
            "annual_mileage": "12000"
        }
    }
    
    try:
        result = await principal_agent.process(vehicle_request)
        print_qc_results("Vehicle Management", result)
    except Exception as e:
        print(f"❌ Error in vehicle test: {e}")
    
    # Test Case 4: Multi-Domain Request (All Experts)
    print("\n🌐 Test Case 4: Multi-Domain Request (All Experts)")
    print("-" * 40)
    
    multi_domain_request = {
        "request_id": f"multi_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "user_id": "user_004",
        "request_type": "comprehensive_analysis",
        "description": "I need comprehensive analysis covering utility optimization, financial planning, and vehicle management. I want to reduce all my expenses and improve efficiency across all areas.",
        "metadata": {
            "property_type": "residential",
            "monthly_income": "$6000",
            "vehicle_count": 2,
            "current_expenses": "$4000/month"
        }
    }
    
    try:
        result = await principal_agent.process(multi_domain_request)
        print_qc_results("Multi-Domain", result)
    except Exception as e:
        print(f"❌ Error in multi-domain test: {e}")
    
    # Cleanup
    await principal_agent.cleanup()
    print("\n✅ Quality Check Flow Test Completed")

def print_qc_results(test_name: str, result: dict):
    """Print quality check results in a formatted way."""
    
    print(f"\n📋 {test_name} - Quality Check Results:")
    print(f"   Request ID: {result.get('request_id', 'N/A')}")
    print(f"   Processing Time: {result.get('processing_time', 0):.2f}s")
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

def print_detailed_qc_report(result: dict):
    """Print detailed quality check report for debugging."""
    
    print("\n🔍 DETAILED QUALITY CHECK REPORT")
    print("=" * 60)
    
    # Print expert quality assessments
    quality_assessments = result.get('quality_assessments', {})
    for expert_name, qc_report in quality_assessments.items():
        print(f"\n📋 {expert_name.upper()} QUALITY REPORT:")
        print(f"   Agent: {qc_report.agent_name}")
        print(f"   Overall Score: {qc_report.overall_score:.3f}")
        print(f"   Quality Level: {qc_report.quality_level.value}")
        print(f"   Passed Threshold: {qc_report.passed_threshold}")
        print(f"   Approved for Publication: {qc_report.approved_for_publication}")
        print(f"   Total Issues: {qc_report.total_issues}")
        print(f"   Total Recommendations: {qc_report.total_recommendations}")
        print(f"   Summary: {qc_report.summary}")
        
        # Print individual metrics
        print(f"\n   📊 Quality Metrics:")
        for metric in qc_report.metrics:
            print(f"      {metric.dimension.value}: {metric.score:.3f} (weight: {metric.weight})")
            print(f"         Description: {metric.description}")
            if metric.issues:
                print(f"         Issues: {', '.join(metric.issues)}")
            if metric.recommendations:
                print(f"         Recommendations: {', '.join(metric.recommendations)}")
    
    # Print final synthesis QC
    final_qc = result.get('final_quality_report')
    if final_qc:
        print(f"\n🎯 FINAL SYNTHESIS QUALITY REPORT:")
        print(f"   Overall Score: {final_qc.overall_score:.3f}")
        print(f"   Quality Level: {final_qc.quality_level.value}")
        print(f"   Passed Threshold: {final_qc.passed_threshold}")
        print(f"   Approved for Publication: {final_qc.approved_for_publication}")
        print(f"   Summary: {final_qc.summary}")

async def main():
    """Main function to run the QC flow test."""
    try:
        await test_qc_flow()
        
        # Uncomment the line below to see detailed QC reports
        # print_detailed_qc_report(result)
        
    except Exception as e:
        logger.error(f"Error in QC flow test: {e}")
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 