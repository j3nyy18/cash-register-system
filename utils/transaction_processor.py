from utils.wallet_manager import deduct_wallet
from utils.discount_engine import apply_discounts
from utils.cashback_engine import calculate_cashback
from utils.json_storage_manager import get_user, update_user
import datetime


def process_transaction(phone, bill_amount, promo_code=None):

    if bill_amount <= 0:
        return {"success": False, "error": "Bill amount must be greater than zero"}

    user = get_user(phone)

    if not user:
        return {"success": False, "error": "User not found"}

    final_amount, discounts_applied, gst = apply_discounts(
        user,
        bill_amount,
        promo_code
    )
    if final_amount is None:
        return {"success": False, "error": "Discount calculation failed"}

    wallet_result = deduct_wallet(phone, final_amount)

    if not wallet_result["success"]:
        return {"success": False, "error": wallet_result["error"]}

    cashback = calculate_cashback(final_amount)

    user = get_user(phone)
    user["wallet_balance"] = round(user["wallet_balance"] + cashback, 2)

    transaction = {
        "original_bill": bill_amount,
        "discounts_applied": discounts_applied,
        "gst": gst,
        "final_bill": final_amount,
        "cashback": cashback,
        "date_time": str(datetime.datetime.now())
    }

    user["transactions"].append(transaction)
    user["last_transaction"] = transaction["date_time"]

    update_user(user)

    return {"success": True, "data": transaction}