from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os

# Cargar archivo cont.env desde la misma carpeta que app.py
env_path = Path(__file__).parent / "cont.env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__, template_folder='templates')

# Leer variables de entorno
mongo_host = os.getenv("MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
mongo_user = os.getenv("MONGO_USER")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_db = os.getenv("MONGO_DB")
mongo_uri = os.getenv("MONGO_URI")

# Validación básica de variables
if not all([mongo_host, mongo_port, mongo_user, mongo_password, mongo_db]):
    raise EnvironmentError("Faltan variables de entorno en cont.env")

# Convertir puerto a entero
mongo_port = int(mongo_port)

# Construir URI de conexión
# mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}?authSource=admin"
mongo_uri ={mongo_uri}
client = MongoClient(mongo_uri)
db = client[mongo_db]

# Ruta básica
@app.route('/')
def metodo():
    return 'Hola mundo'

# Ingreso de datos de wokwi
@app.route('/receive_sensor_data/', methods=['POST'])
def receive_sensor_data():
    datos = request.json

    # Obtener tipo de sensor y normalizar
    sensor_type = datos.get("sensor_type", "desconocido").lower()

    # Insertar en la colección correspondiente
    coleccion = db[sensor_type]
    resultado = coleccion.insert_one(datos)

    print(f"[OK] Dato insertado en colección '{sensor_type}' con ID: {resultado.inserted_id}")
    return jsonify({"insertado_id": str(resultado.inserted_id)}), 201


# Ruta HTML básica
@app.route('/index')
def index():
    return render_template('index.html')

# Ruta para ingresar datos en la base
@app.route('/agregar dato_prueba')
def agregar_dato_prueba():
    usuario = {"nombre": "Luisa", "rol": "cliente", "activo": True}
    existente = db.usuarios.find_one(usuario)

    if existente:
        mensaje = f"Usuario ya existe con ID: {existente.get('_id')}"
        print(f"[INFO] {mensaje}")
    else:
        resultado = db.usuarios.insert_one(usuario)
        mensaje = f"Usuario insertado con ID: {resultado.inserted_id}"
        print(f"[OK] {mensaje}")

    return mensaje


# Ruta para insertar datos en MongoDB
@app.route('/insertar', methods=['POST'])
def insertar():
    datos = request.json
    resultado = db.usuarios.insert_one(datos)
    return jsonify({"insertado_id": str(resultado.inserted_id)})

# Ruta para consultar datos en JSON
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = list(db.usuarios.find({}, {"_id": 0}))
    return jsonify(usuarios)

# Ruta para mostrar datos en tabla HTML
@app.route('/tabla')
def tabla():
    usuarios = list(db.usuarios.find({}, {"_id": 0}))
    return render_template('tabla.html', usuarios=usuarios)

# Ejecutar la app en modo debug
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

