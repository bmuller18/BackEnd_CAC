from flask import Flask, jsonify , request 
import mysql.connector
from flask_cors import CORS 
from config import MYSQL_CONFIG

app = Flask(__name__)
CORS(app)

def connect_to_mysql():
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        print ("Coneccion con exito")
        return conn
    except mysql.connector.Error as e:
        print(f"Error al conectar: {e}")
        return None

@app.route('/books_bd', methods=['GET'] )
def index():
    conn = connect_to_mysql()

    if conn:
        cursor = connect_to_mysql.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM libros")
            libros = cursor.fetchall()
            cursor.close()
            return jsonify(libros)
        except mysql.connector.Error as e:
            print(f"Error de {e}")
            cursor.close()
            conn.close()
            return jsonify({'error': 'Error de consulta'})
    else:
        return jsonify({'error' : 'Error al conectar a la BD'})

    
    

if __name__ == '__main__':
    app.run(debug=True)
