import os
import json
from client.llama_client import call_llm
from client.mcp_client import call_mcp

def main():

    folder_path = "Cards\Cards_new"

    for file in sorted(os.listdir(folder_path)):

        if file.endswith((".png", ".jpg", ".jpeg")):

            image_path = os.path.join(folder_path, file).replace("\\", "/")

            print("\nProcessing card:", image_path)

            # Agent 1 → Extract visiting card details
            prompt = f"""
A user uploaded a visiting card image.

Extract the following details:
- name
- email
- phone
- designation
- organization

Respond ONLY in JSON format:

{{
  "action": "extract_contact_details",
  "parameters": {{
    "image_path": "{image_path}"
  }}
}}
"""

            response = call_llm(prompt)
            print("LLM Response:", response)

            tool_call = json.loads(response)

            result = call_mcp(
                tool_call["action"],
                tool_call["parameters"]
            )

            print("MCP Result:", result)

            if result["status"] == "error":
                print("MCP ERROR:", result["error"])
                continue

            data = result["result"]

            name = data.get("name", "")
            email = data.get("email", "")
            phone = data.get("phone", "")
            designation = data.get("designation", "")
            organization = data.get("organization", "")

            print("Extracted Details:", data)

            # Email
            email_body = f"""
Dear {name},

Greetings from CDAC Hyderabad.

We are pleased to invite you to the
CDAC Hyderabad Foundation Day celebration.

Your presence would be an honor.

Best regards,
CDAC Hyderabad
"""

            call_mcp(
                "send_email",
                {
                    "to_email": email,
                    "subject": "CDAC Hyderabad Foundation Day Invitation",
                    "body": email_body
                }
            )

            

            
if __name__ == "__main__":
    main()