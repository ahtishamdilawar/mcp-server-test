from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import os

app = FastAPI(title="Simple MCP Server")

# Define available tools
TOOLS = [
    {
        "name": "echo",
        "description": "Echoes back the input message",
        "inputSchema": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to echo back"
                }
            },
            "required": ["message"]
        }
    },
    {
        "name": "add",
        "description": "Adds two numbers together",
        "inputSchema": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "multiply",
        "description": "Multiplies two numbers",
        "inputSchema": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            "required": ["a", "b"]
        }
    }
]

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "server": "simple-mcp-server",
        "version": "1.0.0"
    }

@app.get("/tools")
async def list_tools():
    """List available tools."""
    return {"tools": TOOLS}

@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, request: Request):
    """Execute a tool."""
    try:
        body = await request.json()
        arguments = body.get("arguments", {})
        
        if tool_name == "echo":
            message = arguments.get("message", "")
            return {"result": f"Echo: {message}"}
        
        elif tool_name == "add":
            a = arguments.get("a", 0)
            b = arguments.get("b", 0)
            result = a + b
            return {"result": f"Result: {result}", "value": result}
        
        elif tool_name == "multiply":
            a = arguments.get("a", 1)
            b = arguments.get("b", 1)
            result = a * b
            return {"result": f"Result: {result}", "value": result}
        
        else:
            return JSONResponse(
                status_code=404,
                content={"error": f"Tool '{tool_name}' not found"}
            )
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
