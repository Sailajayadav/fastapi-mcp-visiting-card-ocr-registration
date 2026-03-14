from dotenv import load_dotenv
import os
import json
import re
import pandas as pd
import cv2
from paddleocr import PaddleOCR
from openai import OpenAI
# Load environment variables
load_dotenv()

# -------------------------------
# Initialize PaddleOCR
# -------------------------------

ocr = PaddleOCR(use_angle_cls=True, lang="en")

# -------------------------------
# Initialize Qwen LLM Client
# -------------------------------

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_API_KEY")
)

# -------------------------------
# Fallback Regex Extraction
# -------------------------------

def fallback_extract(text):

    email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phone = re.findall(r"\+?\d[\d\s\-]{8,}", text)

    return {
        "Name": "",
        "Email": email[0] if email else "",
        "Phone": phone[0] if phone else "",
        "Designation": "",
        "Organization": ""
    }

# -------------------------------
# LLM Extraction Function
# -------------------------------

def extract_with_qwen(text_list):

    text = "\n".join(text_list)

    prompt = f"""
Extract the following fields from the visiting card text.

Return ONLY JSON.

Fields:
Name
Email
Phone
Designation
Organization

JSON format:

{{
 "Name": "",
 "Email": "",
 "Phone": "",
 "Designation": "",
 "Organization": ""
}}

Text:
{text}
"""

    try:

        completion = client.chat.completions.create(
            model="Qwen/Qwen2.5-7B-Instruct:featherless-ai",
            messages=[
                {"role": "system", "content": "Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        response = completion.choices[0].message.content

        # Extract JSON safely
        json_match = re.search(r"\{.*\}", response, re.DOTALL)

        if json_match:

            json_text = json_match.group()

            return json.loads(json_text)

        else:

            print("⚠ JSON not found in LLM response")

            return fallback_extract(text)

    except Exception as e:

        print("⚠ LLM failed:", e)

        return fallback_extract(text)

# -------------------------------
# OCR + LLM Processing
# -------------------------------

def extract_contact_details(image_path):

    img = cv2.imread(image_path)

    if img is None:
        print("❌ Could not read image:", image_path)
        return None

    results = ocr.ocr(img)

    if not results or not results[0]:
        print("⚠ No text detected")
        return None

    text_list = []

    for line in results[0]:

        text = line[1][0]

        text_list.append(text)

    print("OCR Text:", text_list)

    data = extract_with_qwen(text_list)

    return data

# -------------------------------
# Process All Cards
# -------------------------------

def process_cards(folder="Cards/Cards_new"):

    contacts = []

    if not os.path.exists(folder):
        print("❌ Cards folder not found")
        return contacts

    for file in sorted(os.listdir(folder)):

        if file.lower().endswith((".png", ".jpg", ".jpeg")):

            image_path = os.path.join(folder, file)

            print("\nProcessing:", image_path)

            data = extract_contact_details(image_path)

            if data:
                contacts.append(data)

    return contacts

# -------------------------------
# Save to Excel
# -------------------------------

def save_to_excel(data, file_name="contacts.xlsx"):

    if not data:
        print("No contacts extracted.")
        return

    df = pd.DataFrame(data)

    df.to_excel(file_name, index=False)

    print("\n✅ Excel file created:", file_name)

# -------------------------------
# Main
# -------------------------------

if __name__ == "__main__":

    contacts = process_cards()

    save_to_excel(contacts)