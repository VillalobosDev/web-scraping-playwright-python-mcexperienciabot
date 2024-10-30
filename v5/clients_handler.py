from config import clientes, clientesusados

def get_first_client():
    try:
        with open(clientes, "r", encoding='utf-8') as file:
            lines = file.readlines()
            if lines:
                client_info = lines[0].strip()
                with open(clientes, "w", encoding='utf-8') as updated_file:
                    updated_file.writelines(lines[1:])
                return client_info
            else:
                print("No more clients in the file.")
                return None
    except FileNotFoundError:
        print(f"Error: {clientes} file not found.")
        return None
    except Exception as e:
        print(f"An error occurred while getting client info: {e}")
        return None

def move_client_to_used(client_info):
    try:
        with open(clientesusados, "a", encoding='utf-8') as used_file:
            used_file.write(client_info + "\n")
    except FileNotFoundError:
        print(f"Error: {clientesusados} file not found.")
    except Exception as e:
        print(f"An error occurred while moving client info to the used file: {e}")
