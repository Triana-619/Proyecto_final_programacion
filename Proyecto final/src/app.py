from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os

# Cargar archivo cont.env desde la misma carpeta que app.py
env_path = Path(__file__).parent / "cont.env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

# Leer variables de entorno
mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB")

# Validación básica
if not all([mongo_uri, mongo_db]):
    raise EnvironmentError("Faltan variables de entorno en cont.env")

# Conexión a MongoDB Atlas
client = MongoClient(mongo_uri)
db = client[mongo_db]

# Ruta básica para verificar que el servidor está vivo
@app.route('/')
def home():
    return 'Servidor Flask activo y conectado a MongoDB Atlas'

# Ingreso de datos desde Wokwi
@app.route('/receive_sensor_data/', methods=['POST'])
def receive_sensor_data():
    datos = request.json
    # Normalizamos el nombre del sensor para evitar problemas de mayúsculas/minúsculas
    sensor_type = datos.get("sensor_type", "desconocido").strip().lower()
    coleccion = db[sensor_type]
    resultado = coleccion.insert_one(datos)
    print(f"[OK] Dato insertado en colección '{sensor_type}' con ID: {resultado.inserted_id}")
    return jsonify({"insertado_id": str(resultado.inserted_id)}), 201

# Endpoint para Grafana: consulta datos por tipo de sensor
@app.route('/grafana_data', methods=['GET'])
def grafana_data():
    sensor_type = request.args.get("sensor_type", "desconocido").strip().lower()
    if sensor_type not in db.list_collection_names():
        return jsonify({"error": f"Colección '{sensor_type}' no existe"}), 404
    datos = list(db[sensor_type].find({}, {"_id": 0}))
    return jsonify(datos)

# Ejecutar la app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
