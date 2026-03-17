import json

FILE_PATH = "data/users.json"


def read_data():
    """Read Data from JSON file"""
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}
    except json.JSONDecodeError:
        print("Error: JSON file is corrupted.")
        return {"users": []}
    except Exception as e:
        print(f"Unexpected error while reading data: {e}")
        return {"users": []}


def write_data(data):
    """Write Updated data to JSON file"""
    try:
        with open(FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error writing to JSON file: {e}")


def get_user(phone):
    """Find user by Phone number"""
    try:
        data = read_data()

        for user in data["users"]:
            if user["phone"] == phone:
                return user

        return None
    except Exception as e:
        print(f"Error retrieving User: {e}")
        return None


def add_user(new_user):
    """Add New User to JSON"""
    try:
        data = read_data()
        data["users"].append(new_user)
        write_data(data)
    except Exception as e:
        print(f"Error adding user: {e}")


def update_user(updated_user):
    """Update existing User"""
    try:
        data = read_data()

        for index, user in enumerate(data["users"]):
            if user["phone"] == updated_user["phone"]:
                data["users"][index] = updated_user
                break

        write_data(data)

    except Exception as e:
        print(f"Error updating user: {e}")