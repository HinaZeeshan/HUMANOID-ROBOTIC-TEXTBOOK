import os
import sys

# Ensure backend path is set
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config.settings import settings

print(f"CWD: {os.getcwd()}")
print(f"Env file path (from Settings config): {settings.model_config.get('env_file')}")
print(f"COHERE_API_KEY from settings: '{settings.COHERE_API_KEY}'")
print(f"Is key 'Jbcuk...'? {settings.COHERE_API_KEY == 'Jbcuk5UMlPQTL1I4tC45jQwwrdgH2hGc4YsIOFBF'}")
print(f"Environment variable COHERE_API_KEY: '{os.environ.get('COHERE_API_KEY')}'")
