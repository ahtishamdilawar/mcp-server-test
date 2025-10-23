import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import Response
import uvicorn
import os

# Create MCP server instance
mcp_server = Server("simple-mcp-server")

# Define available tools
@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="echo",
            description="Echoes back the input message",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message to echo back"
                    }
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="add",
            description="Adds two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="multiply",
            description="Multiplies two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        )
    ]

# Handle tool calls
@mcp_server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool execution."""
    if name == "echo":
        message = arguments.get("message", "")
        return [TextContent(type="text", text=f"Echo: {message}")]
    
    elif name == "add":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        result = a + b
        return [TextContent(type="text", text=f"The sum of {a} and {b} is {result}")]
    
    elif name == "multiply":
        a = arguments.get("a", 1)
        b = arguments.get("b", 1)
        result = a * b
        return [TextContent(type="text", text=f"The product of {a} and {b} is {result}")]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

# SSE endpoint handler
async def handle_sse(request):
    """Handle SSE connections from Azure AI Foundry."""
    async with SseServerTransport("/messages") as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options()
        )
    return Response()

# Health check endpoint
async def health_check(request):
    """Health check endpoint."""
    return Response(
        content=json.dumps({
            "status": "healthy",
            "server": "simple-mcp-server",
            "version": "1.0.0"
        }),
        media_type="application/json"
    )

# Create Starlette app
app = Starlette(
    routes=[
        Route("/sse", handle_sse),
        Route("/health", health_check),
        Route("/", health_check),
    ]
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
