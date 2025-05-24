#!C:/Python312/python.exe
# -*- coding: utf-8 -*-
import cgi
import cgitb
import hashlib
import urllib.parse
import sys
from db import conectar

cgitb.enable()

def redirigir(tipo, mensaje):
    texto_codificado = urllib.parse.quote(mensaje)
    sys.stdout.write("Content-Type: text/html\r\n")
    sys.stdout.write("Status: 302 Found\r\n")
    sys.stdout.write(f"Location: /redcomer/logeo.html?tipo={tipo}&texto={texto_codificado}\r\n\r\n")

form = cgi.FieldStorage()
usuario = form.getvalue("usuario")
password = form.getvalue("password")

if not usuario or not password:
    redirigir("error", "Usuario o contraseña no recibidos.")
    exit()

hash_password = hashlib.sha256(password.encode()).hexdigest()

try:
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND password=%s", 
                   (usuario, hash_password))
    resultado = cursor.fetchone()

    if resultado:
        usuario_id = resultado[0]  
        print(f"Set-Cookie: usuario_id={usuario_id}; Path=/; HttpOnly")
        sys.stdout.write("Content-Type: text/html\r\n")
        sys.stdout.write("Status: 302 Found\r\n")
        sys.stdout.write("Location: /redcomer/web.html\r\n\r\n")
    else:
        redirigir("error", "Usuario o contraseña incorrectos.")
except Exception as e:
    redirigir("error", f"Error al iniciar sesión: {str(e)}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
