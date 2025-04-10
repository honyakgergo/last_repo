import random
import numpy as np
import os


def predict_class(image):
    prediction = np.array([[random.uniform(0, 1) for i in range(6)]])
    predicted_class = np.argmax(prediction, axis=1)[0]
    class_labels = {0: "Food_Organics", 1:'Glass', 2:'Metal', 3:'Paper_Cardboard', 4:'Plastic',  5:'Vegetation'}
    return class_labels.get(predicted_class, "Unknown")
