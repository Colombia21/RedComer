#!C:/Python312/python.exe
# -*- coding: utf-8 -*-

import cgi
import cgitb
import html
import sys
import json
from db import conectar
import os
from http import cookies

cgitb.enable()

print("Content-Type: application/json\n")

form = cgi.FieldStorage()
descripcion = html.escape(form.getvalue("descripcion", "").strip())

if not descripcion:
    print(json.dumps({"status": "error", "mensaje": "Descripción vacía"}))
    sys.exit()

try:
    conn = conectar()
    cursor = conn.cursor()

    cookie = cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
    usuario_id = cookie.get("usuario_id")

    if usuario_id is None:
        print(json.dumps({"status": "error", "mensaje": "No has iniciado sesión"}))
        sys.exit()

    usuario_id = int(usuario_id.value)

    cursor.execute(
        "INSERT INTO publicaciones (usuario_id, descripcion) VALUES (%s, %s)",
        (usuario_id, descripcion)
    )
    conn.commit()

    print(json.dumps({"status": "ok", "mensaje": "Publicación guardada"}))

except Exception as e:
    print(json.dumps({"status": "error", "mensaje": str(e)}))

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
