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


path_base = 'C:\\cosas\\Proyecto_TC_WEB\\TC_WEB\\'


@app.route ('/')
@app.route ('/inicio') # Decorador
def inicio (): # función o vista
    return render_template ('index.html')

@app.route('/data')
def data ():
    df = pd.read_csv('data/Advertising.csv')
    sample_data = df[['TV', 'radio', 'newspaper', 'sales']].head(10) 
    sample_data_dict = sample_data.to_dict(orient='records')   
    return render_template('data.html', sample_data=sample_data_dict)

@app.route('/modelo')
def modelo():
    return render_template('modelo.html')

@app.route('/predicciones', methods = ['GET', 'POST'])
def predicciones():
    if request.method == 'GET':
        # Renderiza la plantilla si la solicitud es GET
        return render_template('predicciones.html')

    if request.method == 'POST':
        # Maneja la solicitud POST para predicción
        model = pickle.load(open(path_base + 'ad_model.pkl', 'rb'))

        tv = request.form.get('tv', None)
        radio = request.form.get('radio', None)
        newspaper = request.form.get('newspaper', None)

        if tv is None or radio is None or newspaper is None:
            return jsonify({"error": "Args empty, the data are not enough to predict, STUPID!!!!"}), 400
        else:
            try:
                prediction = model.predict([[float(tv), float(radio), float(newspaper)]])
                return jsonify({'predictions': prediction[0]})
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            

@app.route('/retrain')
def retrain():
    return render_template('retrain.html')


if __name__ == "__main__":
    os.environ ['FLASK_ENV'] = 'development'
    