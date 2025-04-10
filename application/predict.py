from flask import request, jsonify
import numpy as np
from PIL import Image
import io
from application.garbage_classification_model import load_model, predict_class

# Load model once at startup
model = load_model()

def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Convert image to correct format
    image = Image.open(file.stream).convert("RGB")
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)

    # Make prediction
    prediction = predict_class(model, image)

    return jsonify({'class': prediction})
