import easyocr
import re

reader = easyocr.Reader(['en'], gpu=False)

def extract_contact_details(image_path: str):

    results = reader.readtext(image_path)
    text_list = [res[1] for res in results]

    name = ""
    email = ""
    phone = ""
    designation = ""
    organization = ""

    for text in text_list:

        t = text.strip()

        # EMAIL
        if "@" in t:
            email = t.replace(" ", "").strip()

        # PHONE
        if re.search(r"\+?\d[\d\s]{8,15}", t):
            phone = t.strip()

        # DESIGNATION
        if any(word in t.lower() for word in [
            "manager","engineer","director","developer",
            "analyst","officer","lead","consultant",
            "architect","specialist","coordinator",
            "administrator","executive","assistant",
            "associate","founder","co-founder",
            "ceo","cto","cfo","cio",
            "president","vice","vp",
            "head","principal","advisor",
            "scientist","researcher",
            "trainer","mentor","instructor",
            "marketing","sales","product",
            "designer","strategist","planner",
            "supervisor","controller"
        ]):
            designation = t

        # ORGANIZATION
        if any(word in t.lower() for word in [
            "tech","group","solutions","company",
            "capabl","cdac","labs","systems","technologies"
        ]):
            organization = t.replace(":", "").strip()

    # fallback designation (often below name)
    if not designation and len(text_list) > 1:
        designation = text_list[1]

    # NAME detection
    for text in text_list:
        if re.match(r"^[A-Za-z\s]+$", text):
            name = text
            break

    # EMAIL cleanup
    if email and "@" in email:
        domain = email.split("@")[1]

        if "." not in domain:
            common_tlds = ["com","in","org","net","co","ai","io"]

            for tld in common_tlds:
                if domain.endswith(tld):
                    email = email.replace(domain, domain[:-len(tld)] + "." + tld)
                    break

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "designation": designation,
        "organization": organization
    }