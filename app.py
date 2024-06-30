from flask import Flask, jsonify, render_template
import mysql.connector
from flask_cors import CORS
from config import MYSQL_CONFIG

app = Flask(__name__)
CORS(app)

def conectar():
    conexion = mysql.connector.connect(**MYSQL_CONFIG)
    return conexion

def desconectar(conexion):
    if conexion:
        conexion.close()

@app.route('/')
def index():
    conn = conectar()

    if conn:
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM libros")
            libros = cursor.fetchall()
            print(libros)  # Depuración: imprimir los datos obtenidos
            cursor.close()
            desconectar(conn)
            return render_template('index.html', libros=libros)
        except mysql.connector.Error as e:
            print(f"Error de {e}")
            cursor.close()
            desconectar(conn)
            return jsonify({'error': 'Error de consulta'})
    else:
        return jsonify({'error': 'Error al conectar a la BD'})

if __name__ == '__main__':
    app.run(debug=True)
