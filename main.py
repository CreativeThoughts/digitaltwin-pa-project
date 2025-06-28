import uvicorn
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from api.routes import app
from config.settings import settings
from utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    logger.info("Starting Agentic AI Solution...")
    logger.info(f"API Host: {settings.api_host}")
    logger.info(f"API Port: {settings.api_port}")
    logger.info(f"Log Level: {settings.log_level}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Agentic AI Solution...")

# Add lifespan to the app
app.router.lifespan_context = lifespan

@app.get("/swagger.yaml", include_in_schema=False)
def download_swagger_yaml():
    """Serve the OpenAPI YAML spec for download."""
    yaml_path = os.path.join(os.path.dirname(__file__), "swagger.yaml")
    return FileResponse(yaml_path, media_type="application/x-yaml", filename="swagger.yaml")

def main():
    """Main entry point for the application."""
    try:
        logger.info("Initializing Agentic AI Solution...")
        
        # Start the FastAPI server
        uvicorn.run(
            "main:app",
            host=settings.api_host,
            port=settings.api_port,
            reload=False,  # Set to True for development
            log_level=settings.log_level.lower(),
            access_log=True
        )
        
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Error starting application: {e}")
        raise

if __name__ == "__main__":
    main() 