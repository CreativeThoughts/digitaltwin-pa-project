import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from utils.file_streamer import FileStreamer
from loguru import logger


def test_file_streamer_instantiation():
    streamer = FileStreamer()
    assert streamer is not None


class TestLogger:
    """Test cases for logger functionality"""
    
    def test_logger_setup(self):
        """Test logger setup"""
        # Test that logger is available
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'warning')
        assert hasattr(logger, 'debug')
        
    def test_logger_levels(self):
        """Test different logger levels"""
        # Test that logger can handle different levels
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        # If we get here without errors, the test passes
        assert True
        
    def test_logger_file_output(self):
        """Test logger file output"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_filename = temp_file.name
            
        try:
            # Add a temporary file handler
            logger.add(temp_filename, format="{message}")
            logger.info("Test log message")
            
            # Check if message was written to file
            with open(temp_filename, 'r') as f:
                content = f.read()
                assert "Test log message" in content
                
        finally:
            # Remove the temporary handler
            logger.remove()
            os.unlink(temp_filename)


if __name__ == "__main__":
    pytest.main([__file__]) 