from tools.vision_agent import extract_contact_details
from tools.email_service import send_email
from tools.user_store import register_user

TOOLS = {
    "extract_contact_details": extract_contact_details,
    "register_user": register_user,
    "send_email": send_email,

}