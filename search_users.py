#!C:/Python312/python.exe
# -*- coding: utf-8 -*-

import os
import sys
import json
import cgi
from db import conectar


def responder(obj):
    print("Content-Type: application/json\r\n")
    print(json.dumps(obj, ensure_ascii=False))
    sys.exit()


qs = os.environ.get("QUERY_STRING", "")
params = dict(pair.split("=",1) for pair in qs.split("&") if "=" in pair)
q = params.get("q", "").strip()

if not q:
    responder({"status": "ok", "usuarios": []})

try:
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT usuario FROM usuarios WHERE usuario LIKE %s LIMIT 10",
        (f"%{q}%",)
    )
    rows = cursor.fetchall()
    usuarios = [row[0] for row in rows]

    responder({"status": "ok", "usuarios": usuarios})
except Exception as e:
    responder({"status":"error", "mensaje": str(e)})
finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn'   in locals(): conn.close()
