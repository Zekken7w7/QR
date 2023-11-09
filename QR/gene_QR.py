import qrcode
import pandas as pd
import pyodbc

# Configura la conexión a la base de datos SQL Server
server = 'KEVIN_ALBERTO'  # Reemplaza con el nombre de tu servidor SQL Server
database = 'nBD_alumnos'  # Reemplaza con el nombre de tu base de datos
username = 'Kevin_Alberto\kevin_alberto'  # Reemplaza con tu nombre de usuario
password = 'kevin2010'  # Reemplaza con tu contraseña

# Establece la conexión
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = conn.cursor()

# Crear la tabla si no existe
create_table_query = """
CREATE TABLE IF NOT EXISTS Estudiantes (
    ID INT PRIMARY KEY,
    Nombre NVARCHAR(255),
    Edad INT,
    Carrera NVARCHAR(255),
    CodigoQR NVARCHAR(255)
)
"""

cursor.execute(create_table_query)
conn.commit()

# Crear una lista de diccionarios con la información de los estudiantes
estudiantes = [
    {"nombre": "Christopher Soriano", "edad": 20, "carrera": "ICO", "id": 1926638},
    {"nombre": "Kevin Miranda", "edad": 22, "carrera": "ICO", "id": 1926639},
    {"nombre": "Antonio Blancas", "edad": 21, "carrera": "ICO", "id": 1926658},
    # Agrega más estudiantes según sea necesario
]

# Crear un DataFrame de pandas con la información de los estudiantes
df = pd.DataFrame(estudiantes)

# Crear códigos QR y guardar la información en la base de datos
for index, estudiante in df.iterrows():
    data = f"Nombre: {estudiante['nombre']}\nEdad: {estudiante['edad']}\nCarrera: {estudiante['carrera']}\nID: {estudiante['id']}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Insertar los datos en la base de datos
    insert_query = "INSERT INTO Estudiantes (ID, Nombre, Edad, Carrera, CodigoQR) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(insert_query, (estudiante['id'], estudiante['nombre'], estudiante['edad'], estudiante['carrera'], f"codigo_qr_estudiante_{estudiante['id']}.png"))
    conn.commit()

# Cerrar la conexión a la base de datos al finalizar
conn.close()
