from datetime import datetime
from utils.constants import (
    CUSTOMER_OF_MONTH_DISCOUNT,
    WEEKEND_DISCOUNT,
    PROMO_DISCOUNT,
    GST_RATE
)


def apply_discounts(user, amount, promo_code=None):
    try:
        if amount <= 0:
            raise ValueError("Invalid bill amount")
        new_price = amount
        discounts_applied = []
        if user.get("is_customer_of_month"):
            disc = new_price * CUSTOMER_OF_MONTH_DISCOUNT
            new_price -= disc
            discounts_applied.append("Customer of Month 10% Discount")
        if datetime.now().weekday() in [5, 6]:
            disc = new_price * WEEKEND_DISCOUNT
            new_price -= disc
            discounts_applied.append("Weekend 30% Discount")
        if promo_code == "OFF30%":
            disc = new_price * PROMO_DISCOUNT
            new_price -= disc
            discounts_applied.append("Promo Code 30% Discount")
        gst = round(new_price * GST_RATE, 2)
        final_amount = round(new_price + gst, 2)

        return final_amount, discounts_applied, gst

    except Exception as e:
        print(f"Discount calculation error: {e}")
        return None, [], 0