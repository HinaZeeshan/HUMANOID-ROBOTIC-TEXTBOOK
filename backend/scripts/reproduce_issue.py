import sys
import os
import logging

# Add backend directory to path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_dir)

# Mock settings to force invalid API key
from unittest.mock import patch

# Mock the settings module to avoid import errors if .env is missing or invalid
import types
mock_settings = types.ModuleType("settings")
mock_settings.settings = types.SimpleNamespace()
mock_settings.settings.COHERE_API_KEY = "invalid_key"
mock_settings.settings.QDRANT_URL = "http://localhost:6333"
mock_settings.settings.QDRANT_API_KEY = "key"
mock_settings.settings.QDRANT_HOST = "localhost"
mock_settings.settings.QDRANT_PORT = 6333

with patch.dict(sys.modules, {"config.settings": mock_settings}):
    with patch("config.settings.settings", mock_settings.settings):
         # Also patch os.environ just in case it's read directly
        with patch.dict(os.environ, {"COHERE_API_KEY": "invalid_key"}):
            try:
                from services.embedding_service import EmbeddingService
                print("Attempting to initialize EmbeddingService with invalid key...")
                service = EmbeddingService()
                print("EmbeddingService initialized successfully (FIX VERIFIED)")
                
                # Verify that methods handle the missing client gracefully
                print("Testing embed_text with invalid client...")
                result = service.embed_text("test")
                if result == [0.0] * 1024:
                     print("embed_text returned dummy embedding as expected")
                else:
                     print("embed_text returned unexpected result")

            except ValueError as e:
                print(f"Caught ValueError (FIX FAILED): {e}")
            except Exception as e:
                print(f"Caught unexpected exception: {e}")
