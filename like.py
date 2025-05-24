#!C:/Python312/python.exe
# -*- coding: utf-8 -*-

import os
import cgi
import cgitb
import json
from http import cookies
from db import conectar

cgitb.enable()
print("Content-Type: application/json\n")

try:
    form = cgi.FieldStorage()
    publicacion_id = form.getvalue("publicacion_id")
    if not publicacion_id:
        raise ValueError("Falta el parámetro publicacion_id")

    cookie_header = os.environ.get("HTTP_COOKIE", "")
    cookie = cookies.SimpleCookie()
    cookie.load(cookie_header)

    if "usuario_id" not in cookie:
        raise ValueError("No has iniciado sesión")

    usuario_id = cookie["usuario_id"].value

    conn = conectar()
    cursor = conn.cursor()

    # Verificar si el usuario ya dio like
    cursor.execute(
        "SELECT id FROM likes WHERE usuario_id = %s AND publicacion_id = %s",
        (usuario_id, publicacion_id)
    )

    like = cursor.fetchone()

    if like:
        # Si ya dio like, lo quitamos
        cursor.execute(
            "DELETE FROM likes WHERE usuario_id = %s AND publicacion_id = %s",
            (usuario_id, publicacion_id)
        )
        conn.commit()
        resp = {"status": "ok", "accion": "quitar", "mensaje": "Like quitado correctamente"}
    else:
        # Si no dio like, lo insertamos
        cursor.execute(
            "INSERT INTO likes (usuario_id, publicacion_id) VALUES (%s, %s)",
            (usuario_id, publicacion_id)
        )
        conn.commit()
        resp = {"status": "ok", "accion": "agregar", "mensaje": "Like registrado correctamente"}


    cursor.close()
    conn.close()
    print(json.dumps(resp))

except Exception as e:
    print(json.dumps({"status": "error", "mensaje": str(e)}))
