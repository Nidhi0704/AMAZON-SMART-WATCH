## import libraries

from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import joblib
import pandas as pd
import numpy as np

## make an flask app:
app = Flask(__name__)

## load the joblib file
model = joblib.load(open('Watch model.lb','rb'))

## read the csv file:
df = pd.read_csv("Cleaned watch data.csv")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/output')
def output():
    return render_template('output.html')



@app.route('/predict', methods=["GET", "POST"])
@cross_origin()
def predict():
    try:
        Strap_color = request.form.get('Strap_color')
        Size_fits = request.form.get('Size_fits')
        Brand_Name = request.form.get('Brand_Name')
        Screen_Size = request.form.get('Screen_Size')
        Calling_System = request.form.get('Calling_System')

        # Check if any form value is None
        if None in (Strap_color, Size_fits, Brand_Name, Screen_Size, Calling_System):
            return render_template('output.html', prediction_text="Error: Please fill out all fields correctly.")

        # Convert form data to appropriate types
        Strap_color = int(Strap_color)
        Size_fits = int(Size_fits)
        Brand_Name = int(Brand_Name)
        Screen_Size = float(Screen_Size)
        Calling_System = int(Calling_System)

        user_data = [[Strap_color, Size_fits, Brand_Name, Screen_Size, Calling_System]]

        # Predict
        pred = model.predict(user_data)[0]
        prediction = str(round(pred, 2))

        return render_template('output.html', prediction_text=f"The Smart Watch price is around: {prediction}")

    except Exception as e:
        return render_template('output.html', prediction_text=f"Error: {str(e)}")

if  __name__ == "__main__":
    app.run(debug=True)


