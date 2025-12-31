#!/usr/bin/env python3

import sys
from wsgiref.simple_server import make_server
from pathlib import Path

# Add the cgi-bin directory to the path
sys.path.insert(0, str(Path(__file__).parent / 'cgi-bin'))

# Import the WSGI application
from agent_script import application

def create_app():
    """Create a WSGI application that serves static files and CGI scripts"""
    
    def wsgi_app(environ, start_response):
        path = environ['PATH_INFO']
        
        # Serve static files (index.html, etc.)
        if path == '/' or path == '/index.html':
            static_dir = Path(__file__).parent
            file_path = static_dir / 'index.html'
            
            if file_path.exists():
                with open(file_path, 'rb') as f:
                    content = f.read()
                start_response('200 OK', [('Content-Type', 'text/html')])
                return [content]
            else:
                start_response('404 Not Found', [('Content-Type', 'text/plain')])
                return [b"index.html not found"]
        
        # Route CGI script requests
        elif path == '/cgi-bin/agent_script.py':
            return application(environ, start_response)
        
        else:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b"Not found"]
    
    return wsgi_app

if __name__ == '__main__':
    app = create_app()
    server = make_server('localhost', 8000, app)
    print("Serving HTTP on http://localhost:8000/")
    print("Press Ctrl+C to stop the server")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
