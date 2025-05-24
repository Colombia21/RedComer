#!C:/Python312/python.exe
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import sys
import json
from http import cookies
from db import conectar

cgitb.enable()
print("Content-Type: application/json\n")

form = cgi.FieldStorage()
publicacion_id = form.getvalue("publicacion_id")

if not publicacion_id:
    print(json.dumps({"status": "error", "mensaje": "ID de publicación no proporcionado"}))
    sys.exit()

try:
    conn = conectar()
    cursor = conn.cursor()

    # Verificar usuario desde cookie
    cookie = cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
    usuario_cookie = cookie.get("usuario_id")
    if not usuario_cookie:
        print(json.dumps({"status": "error", "mensaje": "No has iniciado sesión"}))
        sys.exit()

    usuario_id = int(usuario_cookie.value)
    publicacion_id = int(publicacion_id)

    # Verificar si la publicación pertenece al usuario
    cursor.execute("SELECT usuario_id FROM publicaciones WHERE id = %s", (publicacion_id,))
    fila = cursor.fetchone()

    if not fila:
        print(json.dumps({"status": "error", "mensaje": "Publicación no encontrada"}))
        sys.exit()

    if fila[0] != usuario_id:
        print(json.dumps({"status": "error", "mensaje": "No puedes eliminar esta publicación"}))
        sys.exit()
    # Eliminar likes asociados a la publicación
    cursor.execute("DELETE FROM likes WHERE publicacion_id = %s", (publicacion_id,))

    # Eliminar la publicación
    cursor.execute("DELETE FROM publicaciones WHERE id = %s", (publicacion_id,))
    conn.commit()

    print(json.dumps({"status": "ok", "mensaje": "Publicación eliminada"}))

except Exception as e:
    print(json.dumps({"status": "error", "mensaje": str(e)}))

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
