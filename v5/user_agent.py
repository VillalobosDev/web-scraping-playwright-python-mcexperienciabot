from config import user_agents_file

def get_user_agents():
    try:
        with open(user_agents_file, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: {user_agents_file} file not found.")
        return []
