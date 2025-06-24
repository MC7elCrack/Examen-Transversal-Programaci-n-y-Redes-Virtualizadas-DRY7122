from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
db = "usuarios.db"

# Crear tabla
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS usuarios (nombre TEXT, clave TEXT)")
conn.commit()
conn.close()

@app.route('/registro', methods=['POST'])
def registro():
    datos = request.json
    nombre = datos['nombre']
    clave_hash = generate_password_hash(datos['clave'])
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("INSERT INTO usuarios VALUES (?, ?)", (nombre, clave_hash))
    conn.commit()
    conn.close()
    return "Usuario registrado"

if __name__ == '__main__':
    app.run(port=5800)
