from fastapi import FastAPI
import subprocess

app = FastAPI()

# Cria conexão com o banco de dados
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="10.5.0.5",
            user="root",
            password="rootpassword",
            database="LAB08"
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Lista de arquivos a serem lidos do HDFS
files = [
    '/lb8/large_file_1.txt',
    '/lb8/large_file_1.txt',
    '/lb8/large_file_1.txt',
    '/lb8/large_file_1.txt',
    '/lb8/large_file_1.txt'
]

hdfs_client = InsecureClient('http://spark-master:9870', user='hdfs')


@app.get("/")
async def root():
    return {"message": "Hello World"}

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
