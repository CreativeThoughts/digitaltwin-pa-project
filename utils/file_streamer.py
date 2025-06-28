import json
import aiofiles
import asyncio
from datetime import datetime, UTC
from typing import Dict, Any
from pathlib import Path
from utils.logger import logger
from config.settings import settings

class FileStreamer:
    """Handles writing responses to file system (temporary solution before API integration)."""
    
    def __init__(self, file_path: str = None):
        self.file_path = file_path or settings.output_file_path
        self._ensure_output_directory()
    
    def _ensure_output_directory(self):
        """Ensure the output directory exists."""
        output_dir = Path(self.file_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory ensured: {output_dir}")
    
    async def write_response(self, response_data: Dict[str, Any]) -> bool:
        """
        Write response data to file asynchronously.
        
        Args:
            response_data: Dictionary containing response information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Add timestamp to response
            response_data["timestamp"] = datetime.now(UTC).isoformat()
            
            # Read existing data if file exists
            existing_data = []
            if Path(self.file_path).exists():
                async with aiofiles.open(self.file_path, 'r') as f:
                    content = await f.read()
                    if content.strip():
                        existing_data = json.loads(content)
            
            # Append new response
            existing_data.append(response_data)
            
            # Write back to file
            async with aiofiles.open(self.file_path, 'w') as f:
                await f.write(json.dumps(existing_data, indent=2, default=str))
            
            logger.info(f"Response written to {self.file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error writing response to file: {e}")
            return False
    
    def write_response_sync(self, response_data: Dict[str, Any]) -> bool:
        """
        Synchronous version of write_response for compatibility.
        
        Args:
            response_data: Dictionary containing response information
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Add timestamp to response
            response_data["timestamp"] = datetime.now(UTC).isoformat()
            
            # Read existing data if file exists
            existing_data = []
            if Path(self.file_path).exists():
                with open(self.file_path, 'r') as f:
                    content = f.read()
                    if content.strip():
                        existing_data = json.loads(content)
            
            # Append new response
            existing_data.append(response_data)
            
            # Write back to file
            with open(self.file_path, 'w') as f:
                json.dump(existing_data, f, indent=2, default=str)
            
            logger.info(f"Response written to {self.file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error writing response to file: {e}")
            return False
    
    async def get_responses(self, limit: int = 100) -> list:
        """
        Retrieve recent responses from file.
        
        Args:
            limit: Maximum number of responses to return
            
        Returns:
            list: List of response dictionaries
        """
        try:
            if not Path(self.file_path).exists():
                return []
            
            async with aiofiles.open(self.file_path, 'r') as f:
                content = await f.read()
                if not content.strip():
                    return []
                
                responses = json.loads(content)
                return responses[-limit:]  # Return last 'limit' responses
                
        except Exception as e:
            logger.error(f"Error reading responses from file: {e}")
            return []

# Global file streamer instance
file_streamer = FileStreamer() 