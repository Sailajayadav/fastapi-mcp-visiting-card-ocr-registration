from fastapi import FastAPI
from mcp_server.registry import TOOLS
from mcp_server.schemas import MCPRequest, MCPResponse

app = FastAPI(title="Pure MCP Server")

@app.post("/execute", response_model=MCPResponse)
def execute_tool(request: MCPRequest):
    action = request.action
    parameters = request.parameters

    if action not in TOOLS:
        return MCPResponse(status="error", error="Unknown tool")

    try:
        result = TOOLS[action](**parameters)
        return MCPResponse(status="success", result=result)
    except Exception as e:
        return MCPResponse(status="error", error=str(e))