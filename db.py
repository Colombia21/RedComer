import sys
sys.path.append(r'C:\Users\zorga\AppData\Roaming\Python\Python312\site-packages')

import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="redcomer"
    )
