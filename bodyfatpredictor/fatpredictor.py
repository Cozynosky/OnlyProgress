import pickle
import pandas as pd

from decimal import *

#model_url = staticfiles_storage.path('data/model.pkl')
model = pickle.load(open("static/data/model.pkl","rb"))
#transformer_url = staticfiles_storage.url('data/transformer.pkl')
transformer = pickle.load(open("static/data/transformer.pkl","rb"))

def predict_bodyfat(bodystats: dict) -> float:
    data = {
        "Age": [bodystats["age"]],
        "Weight": [bodystats["weight"] / Decimal(0.45359237)], # model accepts weight in lbs
        "Height": [bodystats["height"] / Decimal(2.54)], # model accepts height in inchess
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

    density = model.predict(body_stats_df)[0]
    fat = ((4.95/density) - 4.5)*100
    return fat

def calculate_bmi(mass, height):
    return mass / pow(height / 100, 2)
