from utils.json_storage_manager import get_user, update_user



def check_wallet_balance(phone):
    user = get_user(phone)

    if not user:
        return {"success": False, "error": "User not found"}
    
    return {
        "success": True,
        "data": user.get("wallet_balance", 0)
    }


def topup_wallet(phone, amount):

    if amount <= 0:
        return {"success": False, "error": "Amount must be greater than zero"}

    user = get_user(phone)

    if not user:
        return {"success": False, "error": "User not found"}

    user["wallet_balance"] = round(user.get("wallet_balance", 0) + amount, 2)
    update_user(user)

    return {
        "success": True,
        "data": user["wallet_balance"]
    }



def deduct_wallet(phone, amount):

    if amount <= 0:
        return {"success": False, "error": "Invalid deduction amount"}

    user = get_user(phone)

    if not user:
        return {"success": False, "error": "User not found"}

    if user.get("wallet_balance", 0) < amount:
        return {"success": False, "error": "Insufficient balance"}

    user["wallet_balance"] = round(user["wallet_balance"] - amount, 2)
    update_user(user)

    return {
        "success": True,
        "data": user["wallet_balance"]
    }