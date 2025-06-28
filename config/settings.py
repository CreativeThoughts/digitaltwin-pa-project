import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Output Configuration
    output_file_path: str = os.getenv("OUTPUT_FILE_PATH", "./output/responses.json")
    
    # AutoGen Configuration
    autogen_config_list: Optional[list] = None
    
    # Agent Configuration
    max_conversation_turns: int = int(os.getenv("MAX_CONVERSATION_TURNS", "10"))
    timeout: int = int(os.getenv("TIMEOUT", "60"))
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings() 