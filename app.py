from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

ARCHIVO_BD = "sensor.db"

@app.route('/')
def hello_world():
    return '<p> hello world!</p>'

def make_dicts(cursor, row):
    return dict ((cursor.description[idx][0], value)
                 for idx, value in enumerate(row))

@app.route("/api/lecturas")
def lecturas():
    db = sqlite3.connect(ARCHIVO_BD)
    db.row_factory = make_dicts
    resultado = []
    try:
        cursor = db.execute("""SELECT  id,
            nombre, valor,
            daletime(fecha_hor, '-3 hour')
            AS fecha_hora
            FROM lecturas; """)
        resultado = cursor.fetchall()
    finally:
        db.close()
    return jsonify(resultado)

@app.route('/api/sensor', methods=['POST'])
def recibir_datos():
    datos = request.json 
    nombre = datos['nombre']
    valor = datos['valor']

    db = sqlite3.connect(ARCHIVO_BD)
    db.row_factory = make_dicts
    try:
        db.execute(f"""INSERT INTO lecturas (nombre, valor)
                   VALUES(?, ?) """, (nombre, valor))
        db.commit()
    finally:
        db.close()

    return 'OK'
    