from pydantic import BaseModel
from typing import Dict, Any

class MCPRequest(BaseModel):
    action: str
    parameters: Dict[str, Any]

class MCPResponse(BaseModel):
    status: str
    result: Any = None
    error: str = None