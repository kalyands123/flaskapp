import json
import os
from flask import Flask, jsonify

app = Flask(__name__)

# Load JSON data from the given file path
def load_json_data(file_path):
    try:
        with open(file_path, 'r') as f:
            raw_data = f.read()
            # Handle cases where multiple JSON objects are separated by new lines
            data = [json.loads(line) for line in raw_data.splitlines() if line.strip()]
        return data
    except json.JSONDecodeError as e:
        return {"error": f"JSON Decode Error: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

# Path to the source JSON file
json_file_path = r"C:\Users\91901\Downloads\All_Excel_Sheets_Data.json"

# Define a route to accept POST data and save it to the file (POST request)
@app.route('/save-data', methods=['POST'])
def save_data():
    try:
        # Load the JSON data from the file directly
        incoming_data = load_json_data(json_file_path)

        if isinstance(incoming_data, dict) and "error" in incoming_data:
            return jsonify(incoming_data), 400  # Return error if loading failed

        # Define the directory and filename to save the JSON
        save_directory = r"C:\Users\91901\OneDrive\Desktop\Saved"
        save_file_path = os.path.join(save_directory, "All_Employee_Data.json")

        # Create the directory if it doesn't exist
        os.makedirs(save_directory, exist_ok=True)

        # Open the file in append mode and write the new data
        with open(save_file_path, 'a') as f:
            for entry in incoming_data:
                f.write(json.dumps(entry) + '\n')

        return jsonify({"message": "Data successfully saved", "file": save_file_path})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
