import cv2
import datetime
import time  # Importa la biblioteca de tiempo
import numpy as np
from pyzbar.pyzbar import decode
import pandas as pd
import pywhatkit as kit

def leer_codigo_qr(camara, df):
    ret, frame = camara.read()
    datos = None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    codigos_qr = decode(gray)

    for codigo_qr in codigos_qr:
        datos = codigo_qr.data.decode('ISO-8859-1')
        print(f"Código QR: {datos}")

        id_pos = datos.find("ID: ")
        if id_pos != -1:
            id_str = datos[id_pos + 4:].strip()
            try:
                id_numero = int(id_str)
            except ValueError:
                print(f"Error: No se pudo convertir el ID '{id_str}' a un entero.")
                continue

            hora_entrada = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df.loc[df["id"] == id_numero, "Hora_entrada"] = hora_entrada
            cv2.imshow("Lector de QR", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return True, df

    cv2.imshow("Lector de QR", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        return False, df
    elif datos is not None:
        cv2.destroyAllWindows()
        return True, df

    return True, df

if __name__ == "__main__":
    try:
        df = pd.read_excel("BD_alumnos.xlsx")
    except FileNotFoundError:
        print("No se encontró el archivo 'BD_alumnos.xlsx'.")
        exit()

    camara = cv2.VideoCapture(0)

    while True:
        continuar, df = leer_codigo_qr(camara, df)
        if not continuar:
            break

    if df is not None and not df.empty:
        df.to_excel("registro_entradas.xlsx", index=False, engine='openpyxl')

    camara.release()
    cv2.destroyAllWindows()

numero_destino = "+5581420534"
hora_actual = datetime.datetime.now().strftime("%H:%M")
mensaje = f"Hola, usuario registrado. Entrada a las {hora_actual}."
time.sleep(20)  # Agrega un tiempo de espera de 30 segundos
kit.sendwhatmsg(numero_destino, mensaje, datetime.datetime.now().hour, datetime.datetime.now().minute + 1)
