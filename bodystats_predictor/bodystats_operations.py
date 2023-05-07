import pickle
import pandas as pd

from decimal import Decimal

def calculate_bmi(mass, height):
    return mass / pow(height / 100, 2)

def estimate_bodyfat(bmi, age, sex):
    # female - 0, male - 1
    return round((Decimal(1.39) * bmi) + (Decimal(0.16) * age) - (Decimal(10.34) * sex) - 9, 2)

def get_weight_status(bmi) -> str:
    if bmi < 18.5:
        return "under weight"
    elif bmi < 24.9:
        return "normal weight"
    elif bmi < 29.9:
        return "over weight"
    elif bmi < 34.9:
        return "obese class I"
    elif bmi < 39.9:
        return "obese class II"
    else:
        return "obese class III"
    
def get_bodyfat_status(bodyfat, sex):
    
    if sex:
        points = [5, 13, 17, 24]
    else:
        points = [13, 20, 24, 31]
    
    if bodyfat < points[0]:
        return "essential"
    elif bodyfat < points[1]:
        return "athletes"
    elif bodyfat < points[2]:
        return "fitness"
    elif bodyfat < points[3]:
        return "average"
    else:
        return "obese"
