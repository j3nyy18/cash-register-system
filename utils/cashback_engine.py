from utils.constants import CASHBACK_RATE


def calculate_cashback(final_amount):
    try:
        if final_amount <= 0:
            raise ValueError("Invalid final amount")

        cashback = final_amount * CASHBACK_RATE
        return round(cashback, 2)

    except Exception as e:
        print(f"Cashback calculation error: {e}")
        return 0