from flask import Blueprint, render_template, jsonify

routes_bp = Blueprint('routes', __name__)

# Ruta principal para mostrar el map
@routes_bp.route('/')
def routes_view():
    return render_template('map.html')

# Ruta para enviar datos de las estaciones (en formato JSON)
@routes_bp.route('/api/stations', methods=['GET'])
def get_stations():
    # Datos de ejemplo
    stations = [
        {"name": "Estación 1", "lat": 4.60971, "lng": -74.08175, "info": "Temperatura promedio: 20°C"},
        {"name": "Estación 2", "lat": 3.43722, "lng": -76.5225, "info": "Temperatura promedio: 25°C"},
        {"name": "Estación 3", "lat": 6.25184, "lng": -75.56359, "info": "Temperatura promedio: 22°C"},
    ]
    return jsonify(stations)
