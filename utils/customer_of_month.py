from utils.json_storage_manager import read_data


def get_customer_of_month():
    try:
        data = read_data()
        best_customer = None
        highest_spending = 0
        most_transactions = 0

        for user in data.get("users", []):
            transactions = user.get("transactions", [])
            total_spending = sum(t.get("final_bill", 0) for t in transactions)
            transaction_count = len(transactions)

            if total_spending > highest_spending:
                best_customer = user
                highest_spending = total_spending
                most_transactions = transaction_count
            elif total_spending == highest_spending:
                if transaction_count > most_transactions:
                    best_customer = user
                    most_transactions = transaction_count

        return best_customer

    except Exception as e:
        print(f"Customer of month calculation error: {e}")
        return None