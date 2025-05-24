#!C:/Python312/python.exe
# -*- coding: utf-8 -*-
import cgi
import cgitb
import hashlib
import urllib.parse
import sys
from db import conectar

cgitb.enable()


form = cgi.FieldStorage()
usuario = form.getvalue("usuario")
correo = form.getvalue("correo")
password = form.getvalue("password")
confirmar = form.getvalue("confirmar_password")


def redirigir(tipo, mensaje):
    texto_codificado = urllib.parse.quote(mensaje)
    sys.stdout.write("Status: 302 Found\r\n")
    sys.stdout.write(f"Location: /redcomer/mensaje.html?tipo={tipo}&texto={texto_codificado}\r\n\r\n")


if not all([usuario, correo, password, confirmar]):
    redirigir("error", "Todos los campos son obligatorios")
    exit()

if password != confirmar:
    redirigir("error", "Las contraseñas no coinciden")
    exit()

try:
    conn = conectar()
    cursor = conn.cursor()

    hash_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("INSERT INTO usuarios (usuario, correo, password) VALUES (%s, %s, %s)", 
                   (usuario, correo, hash_password))
    conn.commit()

    redirigir("exito", "Registro exitoso")
except Exception as e:
    redirigir("error", f"Error al registrar: {str(e)}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
