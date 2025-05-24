#!C:/Python312/python.exe
# -*- coding: utf-8 -*-

import cgi
import os
import json
from http import cookies
from db import conectar

print("Content-Type: application/json\n")

form = cgi.FieldStorage()
producto_id = form.getvalue("producto_id")


usuario_id = None
if "HTTP_COOKIE" in os.environ:
    cookie = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
    if "usuario_id" in cookie:
        usuario_id = cookie["usuario_id"].value


if not usuario_id or not producto_id:
    print(json.dumps({"status": "error", "mensaje": "Faltan datos"}))
    exit()

try:
    conn = conectar()
    cursor = conn.cursor()

    
    cursor.execute("SELECT usuario_id FROM publicaciones WHERE id = %s", (producto_id,))
    resultado = cursor.fetchone()
    if resultado and str(resultado[0]) == str(usuario_id):
        print(json.dumps({"status": "error", "mensaje": "No puedes añadir tus propios productos"}))
        exit()

    
    cursor.execute("""
        SELECT * FROM carrito WHERE usuario_id = %s AND publicacion_id = %s
    """, (usuario_id, producto_id))
    existe = cursor.fetchone()

    if existe:
        print(json.dumps({"status": "ok", "mensaje": "Ya está en el carrito"}))
    else:
        cursor.execute("""
            INSERT INTO carrito (usuario_id, publicacion_id)
            VALUES (%s, %s)
        """, (usuario_id, producto_id))
        conn.commit()
        print(json.dumps({"status": "ok", "mensaje": "Subido al carrito con éxito"}))

except Exception as e:
    print(json.dumps({"status": "error", "mensaje": str(e)}))

finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()
