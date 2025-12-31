#!/usr/bin/env python3

import urllib.parse
import sys
from strands import Agent
from strands.models.gemini import GeminiModel
from strands.types.exceptions import ModelThrottledException

# --- Request Tracking ---
request_counter = 0

# --- Model Configuration ---
# API key hardcoded (for prototype purposes only - NOT secure for production)

model = GeminiModel(
    client_args={
        "api_key": api_key, # Use the hardcoded API key
    },
    model_id="gemini-2.5-flash",
    params={
        "temperature": 0.7,
        "max_output_tokens": 2048,
        "top_p": 0.9,
        "top_k": 40
    }
)

agent = Agent(model=model, tools=[])

# --- WSGI Application ---
def application(environ, start_response):
    """WSGI application to handle HTTP requests"""
    global request_counter
    request_counter += 1
    req_id = request_counter
    
    print(f"\n[Request #{req_id}] Incoming {environ['REQUEST_METHOD']} request to {environ['PATH_INFO']}", file=sys.stderr)
    
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            # Read the request body
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            body = environ['wsgi.input'].read(content_length).decode('utf-8')
            
            # Parse the form data
            parsed_data = urllib.parse.parse_qs(body)
            user_query = parsed_data.get('query', [''])[0]
            print(f"[Request #{req_id}] Received user query: {user_query}", file=sys.stderr)
            
            if user_query:
                try:
                    # Run the agent with the user's input
                    agent_response = agent(user_query)
                    print(f"[Request #{req_id}] Agent response: {agent_response}", file=sys.stderr)  # Debug: log response to server console
                    
                    # Send response
                    start_response('200 OK', [('Content-Type', 'text/plain')])
                    return [str(agent_response).encode('utf-8')]
                except ModelThrottledException as e:
                    print(f"[Request #{req_id}] ModelThrottledException: {e}", file=sys.stderr)  # Debug: log error
                    start_response('429 Too Many Requests', [('Content-Type', 'text/plain')])
                    return [f"Rate limit exceeded: {e}".encode('utf-8')]
                except Exception as e:
                    print(f"[Request #{req_id}] Unexpected error during agent call: {e}", file=sys.stderr)  # Debug: log error
                    start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
                    return [f"An unexpected error occurred: {e}".encode('utf-8')]
            else:
                print(f"[Request #{req_id}] No query received", file=sys.stderr)
                start_response('400 Bad Request', [('Content-Type', 'text/plain')])
                return [b"Error: No query received."]
        except Exception as e:
            print(f"[Request #{req_id}] Server error during request processing: {e}", file=sys.stderr)  # Debug: log server error
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [f"Server error: {e}".encode('utf-8')]
    else:
        print(f"[Request #{req_id}] Invalid request method: {environ['REQUEST_METHOD']}", file=sys.stderr)
        start_response('405 Method Not Allowed', [('Content-Type', 'text/plain')])
        return [b"Only POST requests are allowed"]