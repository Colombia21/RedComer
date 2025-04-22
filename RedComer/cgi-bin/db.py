import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="tu_usuario",    
        password="tu_password", 
        database="redcomer"
    )
