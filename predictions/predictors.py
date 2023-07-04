import pandas as pd
import numpy as np
import pickle
import cv2
import tensorflow as tf
import os
from decimal import Decimal
from tensorflow import keras
from PIL import Image

from .bodystats_operations import calculate_bmi
from .bmi_data_prepare import find_face, crop_image_to_dimensions
from .bodystats_operations import get_weight_status

PARENT = "D:/Projects/Magisterka/OnlyProgress/"

bodyfat_model = pickle.load(open(PARENT+"static/data/bodyfat_model.pkl","rb"))
transformer = pickle.load(open(PARENT+"static/data/bodyfat_transformer.pkl","rb"))

bmi_model = keras.models.load_model(PARENT+"static/data/bmi_models/bmi_model_36e_0.85")
bmi_classes = pickle.load(open(PARENT+"static/data/bmi_classes.pkl","rb"))


def predict_bodyfat(bodystats: dict) -> float:
    data = {
        "Age": [bodystats["age"]],
        "Weight": [bodystats["weight"] / Decimal(0.45359237)], # bodyfat_model accepts weight in lbs
        "Height": [bodystats["height"] / Decimal(2.54)], # bodyfat_model accepts height in inchess
        "Neck": [bodystats["neck"]],
        "Chest": [bodystats["chest"]],
        "Abdomen": [bodystats["abdomen"]],
        "Hip": [bodystats["hip"]],
        "Thigh": [bodystats["thigh"]],
        "Knee": [bodystats["knee"]],
        "Ankle": [bodystats["ankle"]],
        "Biceps": [bodystats["biceps"]],
        "Forearm": [bodystats["forearm"]],
        "Wrist": [bodystats["wrist"]],
        "Bmi": [calculate_bmi(bodystats["weight"], bodystats["height"])],
        "ACratio": [bodystats["abdomen"]/bodystats["chest"]],
        "HTratio": [bodystats["hip"]/bodystats["thigh"]]
    }
    body_stats_df = pd.DataFrame(data=data)
    body_stats_df = transformer.transform(body_stats_df)

    density = bodyfat_model.predict(body_stats_df)[0]
    fat = ((4.95/density) - 4.5)*100
    return fat

def predict_bmi(input_img, get_class_name=False):
    faces = find_face(input_img, 0.1)
        
    for (x1, y1, x2, y2) in faces:
        cv2.rectangle(input_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            
        face = crop_image_to_dimensions(input_img, x1, y1, x2, y2)
            
        img = Image.fromarray(face, 'RGB')
        img = img.resize((180, 180))
            
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
            
        predictions = bmi_model.predict(img_array, verbose=0)
        score = tf.nn.softmax(predictions[0])
            
        text = f"{bmi_classes[np.argmax(score)]} {round(100 * np.max(score), 2)}%"
        font = cv2.FONT_HERSHEY_SIMPLEX
            
        input_img = cv2.putText(input_img, text, (x1, y1-10), font, 
                   1, (0, 0, 255), 2, cv2.LINE_AA)
        
    if get_class_name:
        return input_img, bmi_classes[np.argmax(score)], round(100 * np.max(score), 2)
    return input_img
    

def predict_bmi_demo():
    
    vid = cv2.VideoCapture(0)
    
    while (True):
        ret, frame = vid.read()
        
        frame = predict_bmi(frame)
  
        # Display the resulting frame
        cv2.imshow('frame', frame)
      
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
    
def predict_bmi_test():
    bmi_dict = {
        "under_weight" : "< 18.5",
        "normal_weight": "18.5 - 24.9",
        "over_weight": "25.0 - 29.9",
        "obese_class_I": "30.0 - 34.9",
        "obese_class_II": "35.0 - 39.9",
        "obese_class_III": " > 40",
    }
    
    for img_name in os.listdir(PARENT + "static/data/downloaded/test_images/"):
        img_path = PARENT + "static/data/downloaded/test_images/" + img_name
        height, weight, name = img_name.split(".")[0].split("_")
        height = int(height)
        weight = int(weight)

        bmi = round(weight / pow(height / 100, 2), 2)
        
        img = cv2.imread(img_path)
        img, class_name, confidence = predict_bmi(img, True)
        cv2.imshow("img", img)
        cv2.waitKey(0)
        
        print(f"weight:{weight}, height: {height}, bmi:{bmi} ({get_weight_status(bmi)}) - predicted class: {class_name} ({bmi_dict[class_name]}) with {confidence}% -- {name}")

    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    predict_bmi_test()