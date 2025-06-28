from fastapi import FastAPI, HTTPException, BackgroundTasks, APIRouter
from datetime import datetime
import uuid
from typing import Dict, Any

from api.models import (
    RequestModel, 
    ResponseModel, 
    HealthResponse,
    RequestType,
    PrincipalAgentResponseModel
)
from agents.principal_agent import PrincipalAgent
from utils.logger import logger
from utils.file_streamer import file_streamer

# Initialize FastAPI app
app = FastAPI(
    title="Agentic AI Solution",
    description="Multi-agent orchestration system using AutoGen framework",
    version="1.0.0"
)

# Initialize principal agent
principal_agent = PrincipalAgent()

router = APIRouter()

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup."""
    try:
        logger.info("Starting Agentic AI Solution...")
        logger.info("Initializing principal agent...")
        await principal_agent.initialize()
        logger.info("Principal agent initialized successfully")
        
        # Verify initialization
        status = principal_agent.get_status()
        logger.info(f"Principal agent status: {status}")
        
        if not status.get("is_initialized", False):
            logger.error("Principal agent initialization failed - is_initialized is False")
            raise RuntimeError("Principal agent initialization failed")
            
        if not status.get("expert_agents"):
            logger.error("Principal agent initialization failed - no expert agents available")
            raise RuntimeError("No expert agents available after initialization")
            
        logger.info("Agentic AI Solution started successfully")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Agentic AI Solution...")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0"
    )

@router.post('/process', response_model=PrincipalAgentResponseModel)
async def process_request(request: RequestModel):
    try:
        result = await principal_agent.process(request.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/request", response_model=ResponseModel)
async def submit_request(
    request: RequestModel,
    background_tasks: BackgroundTasks
):
    """
    Submit a new request for processing by the agentic system.
    
    This endpoint accepts a request and immediately returns an acknowledgment.
    The actual processing is handled asynchronously by the principal agent.
    """
    try:
        logger.info(f"Received request: {request.request_id} of type: {request.request_type}")
        
        # Generate processing ID
        processing_id = str(uuid.uuid4())
        
        # Add request to background processing
        background_tasks.add_task(
            process_request_async,
            request.dict(),
            processing_id
        )
        
        # Return immediate acknowledgment
        response = ResponseModel(
            request_id=request.request_id,
            status="accepted",
            message=f"Request accepted for processing. Processing ID: {processing_id}",
            timestamp=datetime.utcnow().isoformat(),
            processing_id=processing_id
        )
        
        logger.info(f"Request {request.request_id} accepted for processing")
        return response
        
    except Exception as e:
        logger.error(f"Error processing request {request.request_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_request_async(request_data: Dict[str, Any], processing_id: str):
    """
    Process request asynchronously using the principal agent.
    
    Args:
        request_data: Request data dictionary
        processing_id: Unique processing identifier
    """
    try:
        logger.info(f"Starting async processing for request: {request_data['request_id']}")
        # Ensure request_type is a string
        if hasattr(request_data.get('request_type'), 'value'):
            request_data['request_type'] = request_data['request_type'].value
        # Ensure principal agent is initialized in this context
        if not principal_agent.is_initialized:
            logger.warning("Principal agent not initialized in background task. Initializing now...")
            await principal_agent.initialize()
        # Process request with principal agent
        result = await principal_agent.process_request(request_data)
        
        # Prepare response data for file streamer
        response_data = {
            "processing_id": processing_id,
            "request_id": request_data["request_id"],
            "user_id": request_data["user_id"],
            "request_type": request_data["request_type"],
            "status": "completed",
            "result": result,
            "processing_time": result.get("processing_time", 0),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Write response to file streamer
        await file_streamer.write_response(response_data)
        
        logger.info(f"Request {request_data['request_id']} processed successfully")
        
    except Exception as e:
        logger.error(f"Error in async processing for request {request_data['request_id']}: {repr(e)}")
        
        # Write error response to file streamer
        error_response = {
            "processing_id": processing_id,
            "request_id": request_data["request_id"],
            "user_id": request_data["user_id"],
            "request_type": request_data["request_type"],
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await file_streamer.write_response(error_response)

@app.get("/api/responses")
async def get_responses(limit: int = 100):
    """
    Retrieve recent responses from the file streamer.
    
    Args:
        limit: Maximum number of responses to return (default: 100)
    
    Returns:
        List of recent responses
    """
    try:
        responses = await file_streamer.get_responses(limit)
        return {"responses": responses, "count": len(responses)}
    except Exception as e:
        logger.error(f"Error retrieving responses: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agents/status")
async def get_agents_status():
    """Get status of all registered agents."""
    try:
        # Do not await a synchronous method
        status = principal_agent.get_agents_status()
        return status
    except Exception as e:
        logger.error(f"Error getting agents status: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 