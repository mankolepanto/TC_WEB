from flask import Flask, render_template, url_for, request, redirect, jsonify
import os
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import numpy as np
import subprocess


app = Flask (__name__)


path_base = 'C:\\Users\\annav\\THEBRIDGE\\TC_WEB\\'


@app.route ('/')
@app.route ('/inicio') # Decorador
def inicio (): # función o vista
    return render_template ('index.html')

@app.route('/data')
def data ():
    df = pd.read_csv('data/wines_dataset.csv', sep = "|")
    sample_data = df[['class', 'volatile acidity', 'citric acid', 'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol', 'quality']].head(10) 
    sample_data_dict = sample_data.to_dict(orient='records')   
    return render_template('data.html', sample_data=sample_data_dict)

@app.route('/modelo')
def modelo():
    return render_template('modelo.html')

@app.route('/predicciones', methods=['GET', 'POST'])
def predicciones():
    if request.method == 'GET':
        # Renderiza la plantilla si la solicitud es GET
        return render_template('predicciones.html')

    if request.method == 'POST':
        try:
            # Maneja la solicitud POST para predicción
            model = pickle.load(open(path_base + 'ad_model.pkl', 'rb'))

            # Obtiene los valores del formulario
            wine_class = request.form.get('class', None)
            volatile_acidity = request.form.get('volatile_acidity', None)
            citric_acid = request.form.get('citric_acid', None)
            chlorides = request.form.get('chlorides', None)
            free_sulfur_dioxide = request.form.get('free_sulfur_dioxide', None)
            total_sulfur_dioxide = request.form.get('total_sulfur_dioxide', None)
            density = request.form.get('density', None)
            ph = request.form.get('ph', None)
            sulphates = request.form.get('sulphates', None)
            alcohol = request.form.get('alcohol', None)

            # Verifica si alguno de los campos está vacío
            if any(value is None for value in [wine_class, volatile_acidity, citric_acid, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol]):
                return jsonify({"error": "Args empty, the data are not enough to predict"}), 400

            # Convierte los valores a float y usa los nombres de características correctos
            features = {
                'class': wine_class,
                'volatile acidity': float(volatile_acidity),
                'citric acid': float(citric_acid),
                'chlorides': float(chlorides),
                'free sulfur dioxide': float(free_sulfur_dioxide),
                'total sulfur dioxide': float(total_sulfur_dioxide),
                'density': float(density),
                'pH': float(ph),
                'sulphates': float(sulphates),
                'alcohol': float(alcohol)
            }
            
            # Convierte 'white' y 'red' a valores numéricos y añade al DataFrame
            if wine_class.lower() == 'white':
                features['class'] = 1
            elif wine_class.lower() == 'red':
                features['class'] = 0
            else:
                return jsonify({"error": "Invalid value for class"}), 400
            
            # Crea un DataFrame con los nombres de las características
            input_data = pd.DataFrame([features])

            # Realiza la predicción
            prediction = model.predict(input_data)
            prediction = int(prediction[0])
            return jsonify({'predictions': prediction})

        except Exception as e:
            return jsonify({"error": str(e)}), 500
                           

@app.route('/retrain')
def retrain():
    return render_template('retrain.html')


if __name__ == "__main__":
    os.environ ['FLASK_ENV'] = 'development'
    