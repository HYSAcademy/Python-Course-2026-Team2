def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        return ""
    except Exception as e:
        print(f"Error reading file '{path}': {e}")
        return ""