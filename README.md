# Strands AI Agent Web Interface

A web-based chat interface for interacting with Google's Gemini AI model using the Strands agent framework.

## Features

- **Web UI Chat Interface**: Clean, responsive chat interface built with vanilla JavaScript
- **Gemini AI Integration**: Uses Google's Gemini 2.5 Flash model for intelligent responses
- **WSGI Server**: Lightweight Python WSGI server for serving the web interface and handling API requests
- **Request Tracking**: Built-in logging and request tracking for debugging

## Project Structure

```
agents/
├── server.py                 # Main WSGI server
├── index.html               # Web UI (HTML + CSS + JavaScript)
├── cgi-bin/
│   └── agent_script.py     # CGI script handling agent requests
└── venv/                    # Python virtual environment
```

## Prerequisites

- Python 3.8+
- Google Gemini API key

## Installation

1. **Clone or download this repository:**
   ```bash
   cd agents
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install strands
   ```

4. **Set up your API key:**
   - Open `cgi-bin/agent_script.py`
   - Replace the `api_key` variable with your Google Gemini API key
   - For development, the hardcoded key approach is fine
   - For an alternative setup using environment variables, see [Using Environment Variables](#using-environment-variables-alternative) below

## Configuration

### Model Parameters

Edit the model configuration in `cgi-bin/agent_script.py`:

```python
model = GeminiModel(
    client_args={
        "api_key": api_key,
    },
    model_id="gemini-2.5-flash",
    params={
        "temperature": 0.7,
        "max_output_tokens": 2048,
        "top_p": 0.9,
        "top_k": 40
    }
)
```

- **temperature**: Controls randomness (0.0 = deterministic, 1.0 = random)
- **max_output_tokens**: Maximum length of generated responses
- **top_p**: Nucleus sampling parameter
- **top_k**: Number of top tokens to consider

## Running the Server

1. **Activate the virtual environment:**
   ```bash
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```

2. **Start the server:**
   ```bash
   python server.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:8000/`

4. **Stop the server:**
   Press `Ctrl+C` in the terminal

## Usage

1. Type your message in the input field
2. Click "Send" or press Enter
3. Wait for the AI response
4. Continue the conversation

## Architecture

### Server Flow

1. **server.py**: Main WSGI application
   - Serves static HTML files
   - Routes POST requests to the agent script

2. **index.html**: Frontend
   - Chat UI with message history
   - JavaScript fetch API for POST requests
   - Auto-scrolling chat display

3. **cgi-bin/agent_script.py**: Backend
   - Handles POST requests with user queries
   - Processes queries with Gemini model
   - Returns text responses

## Security Notes

⚠️ **Important**: This is a prototype application. For production use:

- Move API keys to environment variables:
  ```python
  import os
  api_key = os.getenv('GEMINI_API_KEY')
  ```
  
- Use HTTPS instead of HTTP
- Implement authentication/authorization
- Add rate limiting
- Use a production WSGI server (e.g., Gunicorn)
- Validate and sanitize user inputs
- Add CORS headers if serving from different domains

## Error Handling

The application includes error handling for:
- Invalid HTTP methods (405)
- Empty queries (400)
- Rate limiting (429)
- AI model errors (500)
- Server errors (500)

Check the browser console (F12) and server terminal for detailed error messages and request logging.

## Troubleshooting

### No response from AI
- Check API key in `cgi-bin/agent_script.py`
- Check server logs for error messages
- Verify internet connection
- Check Gemini API quota

### Port already in use
- Change the port in `server.py`: `make_server('localhost', 8001, app)`

### Module import errors
- Ensure virtual environment is activated
- Run `pip install strands` again
- Check Python version (3.8+)

## Using Environment Variables (Alternative)

If you prefer to use environment variables instead of hardcoding the API key, follow these steps:

### 1. Update `cgi-bin/agent_script.py`

Replace the hardcoded API key line:
```python
# BEFORE
api_key = "AIzaSyBMmDNpXb46IRAVHoRtDie_qenBgx3UST4"
```

With this code that reads from environment variables:
```python
# AFTER
import os

api_key = os.getenv('GEMINI_API_KEY', 'your-api-key-here')
```

The `os.getenv()` function will:
- First check for a `GEMINI_API_KEY` environment variable
- Fall back to the default value if not found
- Raise an error if you need to prompt for a missing key

### 2. Create a `.env` file (Optional)

Create a file named `.env` in the project root:
```
GEMINI_API_KEY=your_actual_api_key_here
```

Then install `python-dotenv` to load it:
```bash
pip install python-dotenv
```

Update the top of `cgi-bin/agent_script.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
```

### 3. Set Environment Variable (No `.env` file)

**On Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your_api_key_here"
python server.py
```

**On Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your_api_key_here
python server.py
```

**On macOS/Linux:**
```bash
export GEMINI_API_KEY="your_api_key_here"
python server.py
```

### 4. Make `.env` file safe

Add `.env` to `.gitignore` (already included) to prevent accidentally committing secrets:
```
.env
.env.local
```

## Dependencies

- **strands**: AI agent framework for working with language models
- **wsgiref**: Python's built-in WSGI reference implementation
- **python-dotenv** (optional): For loading environment variables from `.env` file
