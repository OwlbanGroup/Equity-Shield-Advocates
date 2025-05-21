from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, DashboardHandler)
    print('Starting dashboard server on http://localhost:8000')
    httpd.serve_forever()
