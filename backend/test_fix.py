import sys
import unittest
from unittest.mock import patch, MagicMock
import logging

# We need to mock the environment before importing backend modules to ensure settings are loaded as we expect
with patch.dict('os.environ', {"COHERE_API_KEY": "invalid_key", "QDRANT_URL": "", "QDRANT_API_KEY": ""}):
    try:
        from backend.services.embedding_service import EmbeddingService
    except ImportError:
        # Fallback if running from inside backend dir (not recommended but possible)
        sys.path.append("..")
        from backend.services.embedding_service import EmbeddingService

class TestEmbeddingServiceFix(unittest.TestCase):
    def test_initialization_with_invalid_key(self):
        """Test that EmbeddingService initializes gracefully with an invalid key."""
        print("\nTesting EmbeddingService initialization with invalid key...")
        
        # We need to ensure settings.COHERE_API_KEY is what we want.
        # Check what it is currently
        from backend.config.settings import settings
        print(f"Current settings.COHERE_API_KEY: {settings.COHERE_API_KEY}")
        
        # Force it to be invalid for the test instance
        with patch('backend.config.settings.settings.COHERE_API_KEY', 'invalid_key'):
            try:
                service = EmbeddingService()
                print("SUCCESS: EmbeddingService initialized without raising ValueError.")
                
                # cohere.Client might not raise on init even with invalid key, so client might exist
                # But actual usage should fail gracefully
                
                # Test fail-safe methods
                print("Testing embed_text with invalid client...")
                emb = service.embed_text("test")
                
                # If the key is invalid, the embed() call inside embed_text will raise an exception
                # Our new code should catch it and return dummy embedding
                
                self.assertEqual(len(emb), 1024, "Should return 1024-dim dummy embedding")
                self.assertEqual(emb[0], 0.0, "Should be zero vector")
                
                print("Testing embed_texts with invalid client...")
                embs = service.embed_texts(["test1", "test2"])
                self.assertEqual(len(embs), 2, "Should return 2 embeddings")
                self.assertEqual(len(embs[0]), 1024, "Should be 1024-dim")
                print("SUCCESS: Service methods handled API error gracefully.")
                
            except ValueError as e:
                self.fail(f"EmbeddingService raised ValueError: {e}")
            except Exception as e:
                self.fail(f"EmbeddingService raised unexpected exception: {e}")

if __name__ == "__main__":
    unittest.main()
