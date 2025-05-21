import os
from waitress import serve
from src.api_server import app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure API key is set
if not os.getenv('API_KEY'):
    os.environ['API_KEY'] = 'secret-api-key'

if __name__ == '__main__':
    # Production settings
    host = os.getenv('PRODUCTION_HOST', '0.0.0.0')
    port = int(os.getenv('PRODUCTION_PORT', '8000'))
    threads = int(os.getenv('WAITRESS_THREADS', '4'))
    
    print(f"Starting production server on {host}:{port}")
    print("WARNING: Make sure you have set up your environment variables in .env file")
    
    # Start Waitress production server
    serve(app, host=host, port=port, threads=threads)
