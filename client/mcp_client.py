import requests

MCP_URL = "http://127.0.0.1:8000/execute"

def call_mcp(action, parameters):
    payload = {
        "action": action,
        "parameters": parameters
    }

    response = requests.post(MCP_URL, json=payload)
    return response.json()