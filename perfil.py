#!C:/Python312/python.exe
# -*- coding: utf-8 -*-

import os
import sys
import json
import http.cookies
from db import conectar


def responder(obj):
    sys.stdout.write("Content-Type: application/json\r\n\r\n")
    sys.stdout.write(json.dumps(obj, ensure_ascii=False))
    sys.exit()


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
    
    conn = conectar()
    cursor = conn.cursor()
    debug.append("Conexión BD OK")

    
    cursor.execute("SELECT usuario FROM usuarios WHERE id = %s", (usuario_id,))
    row = cursor.fetchone()
    if not row:
        responder({
            "status": "error",
            "mensaje": "Usuario no encontrado",
            "debug": debug
        })
    usuario_nombre = row[0]
    debug.append(f"Usuario: {usuario_nombre}")

    
    cursor.execute("""
        SELECT p.descripcion,
               COUNT(DISTINCT l.id) AS likes,
               COUNT(DISTINCT c.id) AS añadidos
          FROM publicaciones p
     LEFT JOIN likes l ON l.publicacion_id = p.id
     LEFT JOIN carrito c ON c.publicacion_id = p.id
         WHERE p.usuario_id = %s
      GROUP BY p.id
      ORDER BY p.id DESC
    """, (usuario_id,))
    rows = cursor.fetchall()

    estadisticas = []
    for descripcion, likes, añadidos in rows:
        estadisticas.append({
            "descripcion": descripcion,
            "likes": likes,
            "añadidos": añadidos
        })

   
    cursor.execute("SELECT COUNT(*) FROM likes")
    total_likes = cursor.fetchone()[0] or 0
    debug.append(f"Total likes: {total_likes}")

    cursor.execute("SELECT COUNT(*) FROM carrito")
    total_carrito = cursor.fetchone()[0] or 0
    debug.append(f"Total carrito: {total_carrito}")

    
    responder({
        "status": "ok",
        "usuario": usuario_nombre,
        "total_likes": total_likes,
        "total_carrito": total_carrito,
        "estadisticas": estadisticas,
        "debug": debug
    })

except Exception as e:
    responder({
        "status": "error",
        "mensaje": "Error interno al consultar perfil",
        "debug": debug,
        "detalle": str(e)
    })

finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()
