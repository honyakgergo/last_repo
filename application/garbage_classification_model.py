import tensorflow as tf
import numpy as np
import os

def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))  
    

    model = tf.keras.models.load_model("application/garbage_classification_model.keras", compile=False)
    print(model.summary())
    return model

def predict_class(model, image):
    prediction = model.predict(image)
    print(prediction)
    predicted_class = np.argmax(prediction, axis=1)[0]

    
    class_labels = {0: "Food_Organics", 1:'Glass', 2:'Metal', 3:'Paper_Cardboard', 4:'Plastic',  5:'Vegetation'}
    return class_labels.get(predicted_class, "Unknown")

