from utils.json_storage_manager import get_user, add_user as add_user_to_json, read_data


def add_user(name, phone):

    if not name:
        return {"success": False, "error": "Name cannot be empty"}

    if not phone.isdigit() or len(phone) != 10:
        return {"success": False, "error": "Invalid phone number"}

    existing_user = get_user(phone)

    if existing_user:
        return {"success": False, "error": "User already exists"}

    user = {
        "name": name,
        "phone": phone,
        "wallet_balance": 0,
        "transactions": [],
        "last_transaction": "",
        "is_customer_of_month": False
    }

    add_user_to_json(user)

    return {"success": True, "data": "User added successfully"}



def search_user_by_phone(phone):

    user = get_user(phone)

    if not user:
        return {"success": False, "error": "User not found"}

    return {"success": True, "data": user}



def search_user_by_name(name):

    data = read_data()

    results = [
        user for user in data["users"]
        if user["name"].lower() == name.lower()
    ]

    if not results:
        return {"success": False, "error": "No users found"}

    return {"success": True, "data": results}



def get_user_details(phone):

    user = get_user(phone)

    if not user:
        return {"success": False, "error": "User not found"}

    return {"success": True, "data": user}