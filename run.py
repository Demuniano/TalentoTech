from app import create_app

# Crear la aplicación usando la fábrica
app = create_app()

if __name__ == '__main__':
    # Ejecutar el servidor en modo de desarrollo
    app.run(debug=True, host='127.0.0.1', port=5000)
