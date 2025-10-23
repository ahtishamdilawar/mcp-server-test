# Simple MCP Server for Render

This is a minimal Model Context Protocol (MCP) server using Starlette and the MCP Python SDK, ready to deploy on Render.

Endpoints
- GET /health – simple health check
- GET /sse – establishes the SSE stream for MCP
- POST /messages/ – JSON-RPC message endpoint used by the client after SSE connects

Local run
1) Ensure Python 3.11+
2) Install deps
	pip install -r requirements.txt
3) Start the server
	python server.py
4) Verify
	- Open http://127.0.0.1:8000/health and expect {"status":"healthy", ...}
	- SSE will be available at http://127.0.0.1:8000/sse

Deploy on Render
- This repo includes render.yaml for an auto-deploy web service:
  - Build: pip install -r requirements.txt
  - Start: python server.py
  - Python: 3.11.0
- On render.com:
  1) New > Blueprint Instance
  2) Point to this repo; Render will detect render.yaml
  3) Deploy. Health check at /health will confirm it’s up

Notes
- This server exposes three simple tools: echo, add, multiply
- It uses the SSE transport; many MCP clients support SSE or Streamable HTTP. If you need Streamable HTTP instead, we can switch this to the newer transport.