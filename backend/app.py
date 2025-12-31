from flask import Flask, request, jsonify
import csv
import os

# Initialize Flask app
app = Flask(__name__)

# Define paths for CSV and image storage
DATA_CSV = 'data.csv'
IMAGES_FOLDER = 'uploaded_images'

# Ensure the images folder exists
os.makedirs(IMAGES_FOLDER, exist_ok=True)

# Define a simple route
@app.route('/')
def home():
    return "Backend is running!"

@app.route('/data', methods=['POST'])
def add_data():
    data = request.get_json()

    # Validate JSON content
    if not data or 'type' not in data or 'timestamp' not in data:
        return jsonify({"error": "Invalid data. 'type' and 'timestamp' are required."}), 400

    # Map incoming data to CSV format
    if data['type'] == 'touch':
        new_data = {"name": f"Touch at {data['x']},{data['y']}", "value": data['timestamp']}
    elif data['type'] == 'app':
        new_data = {"name": data['app'], "value": data['timestamp']}
    else:
        return jsonify({"error": "Unsupported data type."}), 400

    # Append data to CSV
    file_exists = os.path.isfile(DATA_CSV)
    with open(DATA_CSV, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "value"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(new_data)

    return jsonify({"message": "Data added successfully!"}), 201

@app.route('/data', methods=['GET'])
def get_data():
    if not os.path.isfile(DATA_CSV):
        return jsonify([])

    # Read data from CSV
    with open(DATA_CSV, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        result = [row for row in reader]

    return jsonify(result)

@app.route('/upload', methods=['POST'])
def upload_image():
    # Debug: Log incoming request
    print("Incoming request to /upload")

    if 'image' not in request.files:
        print("Error: No 'image' field in request files")  # Debug message
        return jsonify({"error": "No image file provided. Use 'image' as the field name."}), 400

    image = request.files['image']
    if image.filename == '':
        print("Error: Empty filename in uploaded file")  # Debug message
        return jsonify({"error": "No selected file."}), 400

    # Save the image to the folder
    image_path = os.path.join(IMAGES_FOLDER, image.filename)
    try:
        image.save(image_path)
        print(f"Image saved successfully at {image_path}")  # Debug message
    except Exception as e:
        print(f"Error saving image: {e}")  # Debug message
        return jsonify({"error": "Failed to save image."}), 500

    return jsonify({"message": "Image uploaded successfully!", "path": image_path}), 201

if __name__ == '__main__':
    app.run(debug=True, port=8000)