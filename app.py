from flask import Flask, jsonify, render_template, request, redirect, url_for
import mysql.connector
from flask_cors import CORS
from config import MYSQL_CONFIG  # Asumiendo que tienes un archivo 'config.py' con la configuración de MySQL

app = Flask(__name__)
CORS(app)  # Permite CORS para la aplicación Flask

# Función para conectar a la base de datos MySQL
def conectar():
    conexion = mysql.connector.connect(**MYSQL_CONFIG)
    return conexion
# Función para desconectar de la base de datos MySQL
def desconectar(conexion):
    if conexion:
        conexion.close()

# Ruta principal que muestra todos los libros desde la base de datos
@app.route('/')
def index():
    conn = conectar()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM libros")
            libros = cursor.fetchall()
            cursor.close()
            desconectar(conn)
            return render_template('index.html', libros=libros)
        except mysql.connector.Error as e:
            print(f"Error de consulta: {e}")
            cursor.close()
            desconectar(conn)
            return jsonify({'error': 'Error de consulta'})
    else:
        return jsonify({'error': 'Error al conectar a la BD'})

# Ruta para mostrar el formulario de creación de libros
@app.route('/create')
def crear():
    # Puedes pasar datos predefinidos aquí si lo deseas
    datos_predefinidos = {
        'titulo': '',
        'autor': '',
        'genero': ''
    }
    return render_template('create.html', datos=datos_predefinidos)

# Ruta para guardar un nuevo libro en la base de datos
@app.route('/guardar', methods=['POST'])
def guardar():
    titulo = request.form['titulo']
    autor = request.form['autor']
    genero = request.form['genero']

    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO libros (title, author, genre) VALUES (%s, %s, %s)", (titulo, autor, genero))
            conn.commit()
            cursor.close()
            desconectar(conn)
            return redirect(url_for('index'))
        except mysql.connector.Error as e:
            print(f"Error al guardar el libro: {e}")
            cursor.close()
            desconectar(conn)
            return jsonify({'error': f'Error al guardar el libro: {e}'})
    else:
        return jsonify({'error': 'Error al conectar a la BD'})

# Ruta para mostrar el formulario de edición de un libro
@app.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    conn = conectar()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM libros WHERE id = %s", (id,))
            libro = cursor.fetchone()
            cursor.close()
            desconectar(conn)
            if libro:
                return render_template('editar.html', libro=libro)
            else:
                return jsonify({'error': 'Libro no encontrado'})
        except mysql.connector.Error as e:
            print(f"Error al obtener el libro para editar: {e}")
            cursor.close()
            desconectar(conn)
            return jsonify({'error': f'Error al obtener el libro para editar: {e}'})
    else:
        return jsonify({'error': 'Error al conectar a la BD'})

# Ruta para actualizar un libro en la base de datos
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    titulo = request.form['titulo']
    autor = request.form['autor']
    genero = request.form['genero']

    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE libros SET title = %s, author = %s, genre = %s WHERE id = %s", (titulo, autor, genero, id))
            conn.commit()
            cursor.close()
            desconectar(conn)
            return redirect(url_for('index'))
        except mysql.connector.Error as e:
            print(f"Error al actualizar el libro: {e}")
            cursor.close()
            desconectar(conn)
            return jsonify({'error': f'Error al actualizar el libro: {e}'})
    else:
        return jsonify({'error': 'Error al conectar a la BD'})

# Ruta para eliminar un libro de la base de datos por su ID
@app.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    conn = conectar()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM libros WHERE id = %s", (id,))
            conn.commit()
            cursor.close()
            desconectar(conn)
            return redirect(url_for('index'))
        except mysql.connector.Error as e:
            print(f"Error al eliminar el libro: {e}")
            cursor.close()
            desconectar(conn)
            return jsonify({'error': f'Error al eliminar el libro: {e}'})
    else:
        return jsonify({'error': 'Error al conectar a la BD'})

if __name__ == '__main__':
    app.run(debug=True)
