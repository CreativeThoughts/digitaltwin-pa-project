import pytest
import json
import os
from fastapi.testclient import TestClient
from main import app
from utils.file_streamer import FileStreamer


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


class TestBasicFunctionality:
    """Basic tests for core functionality"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        
    def test_get_responses(self, client):
        """Test getting responses endpoint"""
        response = client.get("/api/responses")
        assert response.status_code == 200
        data = response.json()
        assert "responses" in data
        assert isinstance(data["responses"], list)
        
    def test_get_responses_with_limit(self, client):
        """Test getting responses with limit parameter"""
        response = client.get("/api/responses?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "responses" in data
        assert len(data["responses"]) <= 5
        
    def test_404_endpoint(self, client):
        """Test 404 handling for non-existent endpoints"""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
        
    def test_method_not_allowed(self, client):
        """Test method not allowed errors"""
        response = client.put("/api/request")
        assert response.status_code == 405


class TestFileStreamer:
    """Test cases for FileStreamer functionality"""
    
    def test_file_streamer_initialization(self):
        """Test FileStreamer initialization"""
        streamer = FileStreamer()
        assert streamer is not None
        # Check that the output directory exists
        assert os.path.exists("output")

    @pytest.mark.asyncio
    async def test_write_and_read_response(self):
        streamer = FileStreamer()
        response_data = {
            "request_id": "test_123",
            "agent_name": "TestAgent",
            "content": "Test response content",
            "timestamp": "2025-06-28T17:00:00Z"
        }
        await streamer.write_response(response_data)
        responses = await streamer.get_responses()
        assert len(responses) > 0
        test_response = None
        for response in responses:
            if response.get("request_id") == "test_123":
                test_response = response
                break
        assert test_response is not None
        assert test_response["agent_name"] == "TestAgent"
        assert test_response["content"] == "Test response content"

    @pytest.mark.asyncio
    async def test_read_responses_with_limit(self):
        streamer = FileStreamer()
        for i in range(3):
            response_data = {
                "request_id": f"limit_test_{i}",
                "agent_name": f"Agent{i}",
                "content": f"Response {i}",
                "timestamp": "2025-06-28T17:00:00Z"
            }
            await streamer.write_response(response_data)
        responses = await streamer.get_responses(limit=2)
        assert len(responses) <= 2


class TestAPIValidation:
    """Test API validation"""
    
    def test_invalid_request_type(self, client):
        """Test submission with invalid request type"""
        request_data = {
            "request_id": "invalid_test",
            "request_type": "INVALID_TYPE",
            "description": "This should fail",
            "user_id": "user_123"
        }
        
        response = client.post("/api/request", json=request_data)
        assert response.status_code == 422  # Validation error
        
    def test_missing_required_fields(self, client):
        """Test submission with missing required fields"""
        request_data = {
            "request_id": "incomplete_test",
            "description": "Missing request_type and user_id"
        }
        
        response = client.post("/api/request", json=request_data)
        assert response.status_code == 422  # Validation error
        
    def test_empty_content(self, client):
        """Test submission with empty content"""
        request_data = {
            "request_id": "empty_test",
            "request_type": "GENERAL",
            "description": "",
            "user_id": "user_123"
        }
        
        response = client.post("/api/request", json=request_data)
        assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    pytest.main([__file__]) 