import pandas as pd
import numpy as np
import pickle
import cv2
import tensorflow as tf
from decimal import Decimal
from tensorflow import keras

from bodystats_operations import calculate_bmi
from bmi_data_prepare import find_face, crop_image_to_dimensions

PARENT = "D:/Projects/Magisterka/OnlyProgress/"
#bodyfat_model_url = staticfiles_storage.path('data/bodyfat_model.pkl')
bodyfat_model = pickle.load(open(PARENT+"static/data/bodyfat_model.pkl","rb"))
#transformer_url = staticfiles_storage.url('data/transformer.pkl')
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

def predict_bmi():
    pass

def predict_bmi_demo():
    
    vid = cv2.VideoCapture(0)
    
    while (True):
        ret, frame = vid.read()
        
        faces = find_face(frame, 0.1)
        
        for (x1, y1, x2, y2) in faces:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            
            face = crop_image_to_dimensions(frame, x1, y1, x2, y2)
            
            cv2.imwrite(PARENT+"static/data/temp/temp_img.jpg", face)
            
            img = tf.keras.utils.load_img(
                PARENT+"static/data/temp/temp_img.jpg", target_size=(180, 180)
            )
            
            img_array = tf.keras.utils.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0) # Create a batch
            
            
            predictions = bmi_model.predict(img_array, verbose=0)
            score = tf.nn.softmax(predictions[0])
            
            text = f"{bmi_classes[np.argmax(score)]} with {round(100 * np.max(score), 2)}%"
            font = cv2.FONT_HERSHEY_SIMPLEX
            
            frame = cv2.putText(frame, text, (x1, y1), font, 
                   1, (0, 0, 255), 2, cv2.LINE_AA)
  
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

if __name__ == "__main__":
    predict_bmi_demo()