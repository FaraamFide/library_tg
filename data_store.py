import json

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            mes_to_execute_and_position = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        mes_to_execute_and_position = {}
        print("JSON file not found or corrupted. Initialized with empty data.")

    return mes_to_execute_and_position 

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        from handlers import mes_to_execute_and_position
        json.dump(mes_to_execute_and_position, file, indent=4, ensure_ascii=False)
    print("Data saved to JSON.")
   
