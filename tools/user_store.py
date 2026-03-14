users = []

def register_user(name: str, email: str):
    user = {"name": name, "email": email}
    users.append(user)
    return f"User {name} registered successfully."