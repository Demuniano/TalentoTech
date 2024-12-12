from flask import Flask, request, render_template, jsonify, Blueprint
import pandas as pd
import sqlite3

routes_bp = Blueprint('routes', __name__)

archivo_entrada = r'app\data\resumen_mensual.csv'
resumen_mensual = pd.read_csv(archivo_entrada)

conn = sqlite3.connect('datos_ambientales.db')
resumen_mensual.to_sql('datos', conn, if_exists='replace', index=False)
conn.close()


# Ruta principal para mostrar el map
@routes_bp.route('/')
def index():
    return render_template('index.html')

@routes_bp.route('/map')
def map():
    return render_template('map.html')
@routes_bp.route('/about')
def about():
    return render_template('about.html')
@routes_bp.route('/InfoModels')
def InfoModels():
    return render_template('InfoModels.html')
def consultar_datos(estaciones, anios, meses, variables):
    if not estaciones or not anios or not meses or not variables:
        return {'error': 'Debe seleccionar al menos una estación, un año, un mes y una variable.'}

    conn = sqlite3.connect('datos_ambientales.db')
    cursor = conn.cursor()

    # Asegurarse de incluir estacion_sk, anio y mes en la consulta
    columnas = ["estacion_sk", "anio", "mes"] + variables
    query = f'''
    SELECT {", ".join(columnas)}
    FROM datos
    WHERE estacion_sk IN ({", ".join(["?"] * len(estaciones))})
    AND anio IN ({", ".join(["?"] * len(anios))})
    AND mes IN ({", ".join(["?"] * len(meses))})
    '''
    parametros = estaciones + anios + meses

    try:
        cursor.execute(query, parametros)
        rows = cursor.fetchall()
        # Crear una lista de diccionarios con nombres de columnas
        result = [
            {columna: value for columna, value in zip(columnas, row)}
            for row in rows
        ]
    except sqlite3.Error as e:
        conn.close()
        return {'error': str(e)}
    conn.close()
    return result


@routes_bp.route('/consultar', methods=['POST'])
def consultar():
    try:
        estaciones = request.form.getlist('estacion')
        anios = [int(anio) for anio in request.form.getlist('anios')]
        meses = [int(mes) for mes in request.form.getlist('meses')]
        variables = request.form.getlist('variables')

        if not estaciones or not anios or not meses or not variables:
            return jsonify({'error': 'Debe seleccionar al menos una estación, un año, un mes y una variable.'}), 400

        datos = consultar_datos(estaciones, anios, meses, variables)

        if 'error' in datos:
            return jsonify(datos), 404

        return jsonify(datos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')