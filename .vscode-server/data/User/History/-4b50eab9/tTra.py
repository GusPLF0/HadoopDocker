from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error
import subprocess
from hdfs import InsecureClient


app = FastAPI()

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="10.5.0.5",
            user="root",
            password="password",
            database="LB08"
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

files = [
    '/lb8/large_file_1.txt',
    '/lb8/large_file_2.txt',
    '/lb8/large_file_3.txt',
    '/lb8/large_file_4.txt',
    '/lb8/large_file_5.txt'
]

hdfs_client = InsecureClient('http://spark-master:9870', user='hdfs')


@app.get("/")
async def root():
    return {"message": "Gustavo here, what's up? ;p "}

@app.get("/micro_servico")
async def root():
    #subprocess.run(["python3", "script_requerido.py"])
    return {"message": "rodou o microserviço com sucesso!"}

@app.post("/line")
def inserir_linha():
    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO documentos (data) VALUES (%s)"
    
    try:
        for file in files:
            with hdfs_client.read(file) as reader:
                for line in reader:
                    data = line.strip()[:20]
                    cursor.execute(query, (data,))
                    connection.commit()
                        
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()
    
    return {"message": "A linha do arquivo foi inserida com sucesso!"}
