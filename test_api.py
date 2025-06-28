#!/usr/bin/env python3
"""
Test script for the Agentic AI Solution API.
This script demonstrates how to use the API with sample requests.
"""

import asyncio
import aiohttp
import json
from datetime import datetime

# API Configuration
API_BASE_URL = "http://localhost:8000"

async def test_health_check():
    """Test the health check endpoint."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/health") as response:
            result = await response.json()
            print("Health Check Result:")
            print(json.dumps(result, indent=2))
            print()

async def test_utility_management_request():
    """Test a utility management request."""
    request_data = {
        "request_id": f"utility_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "user_id": "user_123",
        "request_type": "utility_management",
        "description": "I need help optimizing my energy consumption and reducing utility bills. My electricity usage has been high lately and I want to find ways to save money.",
        "priority": "high",
        "metadata": {
            "current_monthly_bill": "$150",
            "property_type": "residential",
            "occupants": 3
        }
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE_URL}/api/request", json=request_data) as response:
            result = await response.json()
            print("Utility Management Request Result:")
            print(json.dumps(result, indent=2))
            print()
            return result

async def test_financial_health_request():
    """Test a financial health request."""
    request_data = {
        "request_id": f"financial_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "user_id": "user_456",
        "request_type": "financial_health",
        "description": "I want to improve my financial health by creating a better budget and finding ways to save money. I also need help with debt management and investment strategies.",
        "priority": "medium",
        "metadata": {
            "monthly_income": "$5000",
            "current_debt": "$15000",
            "savings_goal": "$10000"
        }
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE_URL}/api/request", json=request_data) as response:
            result = await response.json()
            print("Financial Health Request Result:")
            print(json.dumps(result, indent=2))
            print()
            return result

async def test_vehicle_management_request():
    """Test a vehicle management request."""
    request_data = {
        "request_id": f"vehicle_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "user_id": "user_789",
        "request_type": "vehicle_management",
        "description": "I need help optimizing my vehicle maintenance schedule and reducing fuel costs. I have two cars and want to manage them more efficiently.",
        "priority": "medium",
        "metadata": {
            "vehicles": 2,
            "monthly_fuel_cost": "$300",
            "annual_maintenance_budget": "$2000"
        }
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE_URL}/api/request", json=request_data) as response:
            result = await response.json()
            print("Vehicle Management Request Result:")
            print(json.dumps(result, indent=2))
            print()
            return result

async def test_general_request():
    """Test a general request that should trigger multiple expert agents."""
    request_data = {
        "request_id": f"general_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "user_id": "user_999",
        "request_type": "general",
        "description": "I want to optimize my overall expenses including utilities, vehicle costs, and financial planning. I need a comprehensive analysis of all areas.",
        "priority": "high",
        "metadata": {
            "total_monthly_expenses": "$3000",
            "areas_of_concern": ["utilities", "transportation", "budget"]
        }
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE_URL}/api/request", json=request_data) as response:
            result = await response.json()
            print("General Request Result:")
            print(json.dumps(result, indent=2))
            print()
            return result

async def test_get_responses():
    """Test getting recent responses."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/api/responses?limit=5") as response:
            result = await response.json()
            print("Recent Responses:")
            print(json.dumps(result, indent=2))
            print()

async def test_agents_status():
    """Test getting agents status."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/api/agents/status") as response:
            result = await response.json()
            print("Agents Status:")
            print(json.dumps(result, indent=2))
            print()

async def main():
    """Run all tests."""
    print("=" * 60)
    print("AGENTIC AI SOLUTION - API TEST SCRIPT")
    print("=" * 60)
    print()
    
    try:
        # Test health check
        await test_health_check()
        
        # Wait a moment for the system to be ready
        await asyncio.sleep(2)
        
        # Test specific expert agent requests
        await test_utility_management_request()
        await asyncio.sleep(1)
        
        await test_financial_health_request()
        await asyncio.sleep(1)
        
        await test_vehicle_management_request()
        await asyncio.sleep(1)
        
        # Test general request (should trigger multiple agents)
        await test_general_request()
        await asyncio.sleep(2)
        
        # Test getting responses
        await test_get_responses()
        
        # Test getting agents status
        await test_agents_status()
        
        print("=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Check the output/responses.json file for detailed results.")
        
    except aiohttp.ClientError as e:
        print(f"Error connecting to API: {e}")
        print("Make sure the API server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 