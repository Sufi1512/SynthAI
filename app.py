
from flask import Flask, render_template, request, jsonify
import requests
import io
from PIL import Image
import base64

app = Flask(__name__)

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/stable-diffusion-v1-5/stable-diffusion-v1-5"
headers = {
    "Authorization": "Bearer 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",  # Replace with your API token
}

def query(payload):
    """Send a POST request to the Hugging Face API and return the response content."""
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error querying the API: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/work')
def work():
    return render_template('work.html')

@app.route('/text')
def text():
    return render_template('text_generation.html')

@app.route('/music')
def music():
    return render_template('text_to_music.html')

@app.route('/image')
def generate_image_page():
    return render_template('text_to_image.html')

@app.route('/generate-image', methods=['POST'])
def generate_image():
    """Generate an image based on the description provided by the user."""
    description = request.json.get('description')

    # Make the API request to Hugging Face's model
    image_bytes = query({"inputs": description})

    if image_bytes is None:
        return jsonify({"error": "Failed to generate image"}), 500

    try:
        # Convert the image bytes to a base64 string to send to the frontend
        img = Image.open(io.BytesIO(image_bytes))
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        return jsonify({"image": img_str})
    except Exception as e:
        print(f"Error processing the image: {e}")
        return jsonify({"error": "Image processing failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)

