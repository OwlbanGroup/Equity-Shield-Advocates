# Minimal patch snippet for tests/test_integration.py import fix

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.api_server import create_app

# In your tests/test_integration.py, replace the import section with the above lines
# This will fix the ImportError by correctly importing create_app from src.api_server
