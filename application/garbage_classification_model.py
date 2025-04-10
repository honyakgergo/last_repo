
import numpy as np
import os

 
    


def predict_class(image):
    prediction = model.predict(image)
    print(prediction)
    predicted_class = np.argmax(prediction, axis=1)[0]

    
    class_labels = {0: "Food_Organics", 1:'Glass', 2:'Metal', 3:'Paper_Cardboard', 4:'Plastic',  5:'Vegetation'}
    return class_labels.get(predicted_class, "Unknown")

