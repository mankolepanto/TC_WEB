from flask import Flask, render_template, url_for, request, redirect
import os

app = Flask (__name__)



@app.route ('/')
@app.route ('/inicio') # Decorador
def inicio (): # función o vista
    return render_template ('index.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/modelo')
def modelo():
    return render_template('modelo.html')

@app.route('/retrain')
def retrain():
    return render_template('retrain.html')

if __name__ == "__main__":
    os.environ ['FLASK_ENV'] = 'development'
    