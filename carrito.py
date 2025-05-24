#!C:/Python312/python.exe
# -*- coding: utf-8 -*-

import os
import sys
import json
import http.cookies
from db import conectar

# --- Función para responder JSON y salir ---
def responder(obj):
    sys.stdout.write("Content-Type: application/json\r\n\r\n")
    sys.stdout.write(json.dumps(obj, ensure_ascii=False))
    sys.exit()

# --- Parseo manual de cookies ---
cookie_header = os.environ.get("HTTP_COOKIE", "")
cookies = http.cookies.SimpleCookie()
cookies.load(cookie_header)
if "usuario_id" not in cookies:
    responder({
        "status": "error",
        "mensaje": "Usuario no autenticado",
        "debug": ["Cookie 'usuario_id' ausente"]
    })

usuario_id = cookies["usuario_id"].value
debug = [f"usuario_id: {usuario_id}"]

try:
    # Conexión a la BD
    conn = conectar()
    cursor = conn.cursor()

    debug.append("Conexión BD OK")

    # Verificar usuario
    cursor.execute("SELECT usuario FROM usuarios WHERE id = %s", (usuario_id,))
    row = cursor.fetchone()
    if not row:
        responder({
            "status": "error",
            "mensaje": "Usuario no encontrado",
            "debug": debug + [f"ID inválido: {usuario_id}"]
        })
    usuario_nombre = row[0]
    debug.append(f"Usuario: {usuario_nombre}")

    # Consulta carrito
    cursor.execute("""
        SELECT p.descripcion, c.fecha_agregado
          FROM carrito c
          JOIN publicaciones p ON p.id = c.publicacion_id
         WHERE c.usuario_id = %s
         ORDER BY c.fecha_agregado DESC
    """, (usuario_id,))
    filas = cursor.fetchall()
    debug.append(f"Items en carrito: {len(filas)}")

    publicaciones = []
    for descripcion, fecha in filas:
        publicaciones.append({
            "descripcion": descripcion,
            "fecha": str(fecha),
            "usuario": usuario_nombre
        })

    responder({
        "status": "ok",
        "publicaciones": publicaciones,
        "debug": debug
    })

except Exception as e:
    responder({
        "status": "error",
        "mensaje": "Error interno al consultar carrito",
        "debug": debug,
        "detalle": str(e)
    })

finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()
