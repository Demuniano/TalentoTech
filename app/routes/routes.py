from flask import Flask, request, render_template, jsonify, Blueprint
import pandas as pd
import sqlite3

routes_bp = Blueprint('routes', __name__)
archivo_entrada = r'app\data\resumen_mensual.csv'
resumen_mensual = pd.read_csv(archivo_entrada)

# Ruta principal para mostrar el map
@routes_bp.route('/')
def index():
    return render_template('index.html')

@routes_bp.route('/map')
def map():
    return render_template('map.html')
@routes_bp.route('/InfoModels')
def InfoModels():
    return render_template('InfoModels.html')
def consultar_datos(estaciones, anios, meses, variables):
    # if not estaciones or not anios or not meses or not variables:
    #     return {'error': 'Debe seleccionar al menos una estación, un año, un mes y una variable.'}, 400

    conn = sqlite3.connect('datos_ambientales.db')
    cursor = conn.cursor()

    # Construir la consulta dinámica con múltiples filtros
    query = f'''
    SELECT {", ".join(variables)}
    FROM datos
    WHERE estacion_sk IN ({", ".join(["?"] * len(estaciones))})
    AND anio IN ({", ".join(["?"] * len(anios))})
    AND mes IN ({", ".join(["?"] * len(meses))})
    '''
    
    # Combinar todos los parámetros para la consulta
    parametros = estaciones + anios + meses
    cursor.execute(query, parametros)
    datos = cursor.fetchall()
    conn.close()
    
    # if not datos:
    #     return {'error': 'No se encontraron datos para los criterios seleccionados.'}, 404
    return datos

@routes_bp.route('/consultar', methods=['POST'])
def consultar():
    estaciones = request.form.getlist('estacion')  # Recibir los valores como listas de estaciones
    anios = [int(anio) for anio in request.form.getlist('anios')]  # Recibir los valores como listas de enteros
    meses = [int(mes) for mes in request.form.getlist('meses')]  # Recibir los valores como listas de enteros
    variables = request.form.getlist('variables')  # Lista de variables seleccionadas
    print(estaciones, anios, meses, variables)
    # Verificar que todas las listas tengan al menos un elemento
    # if not estaciones or not anios or not meses or not variables:
    #     return jsonify({'error': 'Debe seleccionar al menos una estación, un año, un mes y una variable.'}), 400

    # Realizar la consulta en SQLite
    datos = consultar_datos(estaciones, anios, meses, variables)

    # if 'error' in datos:
    #     return jsonify(datos), 404

    # Devolver los resultados en formato JSON
    return jsonify(datos)

@routes_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')