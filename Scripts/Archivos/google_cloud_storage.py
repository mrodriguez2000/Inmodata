
# LIBRERIA PARA AUTENTICACION Y CONEXION A GOOGLE CLOUD STORAGE
from google.cloud import storage
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path
import os
import logging

# CARGAR VARIABLES DE ENTORNO
RUTA_ENV = Path(__file__).resolve().parent / ".env"
load_dotenv(RUTA_ENV)


# OBTENER VARIABLES DE ENTORNO
PROJECT_NAME = os.getenv("PROJECT_NAME")
BUCKET_NAME = os.getenv("BUCKET_NAME")


# DEFINIR FUNCIÓN QUE SUBA ARCHIVOS CSV A GOOGLE CLOUD STORAGE
def subir_datos_a_google_cloud_storage(dataframe, nombre_archivo_remoto):
    """
    Sube un archivo CSV a Google Cloud Storage.

    Args:
        dataframe (pd.DataFrame): DataFrame con los datos a subir.
        nombre_archivo_remoto (str): Nombre que tendrá el archivo en el bucket.

    Returns:
        str: Nombre del archivo subido en el bucket.
    """
    try:
        # VALIDAR DATAFRAME
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("Los datos deben ser un DataFrame de pandas.")

        if dataframe.empty:
            raise ValueError("No existen registros para subir.")

        # VALIDAR VARIABLES DE ENTORNO
        if not PROJECT_NAME or not BUCKET_NAME:
            raise ValueError(
                "No se encontraron PROJECT_NAME o BUCKET_NAME."
            )

        # CREAR CLIENTE DE GOOGLE CLOUD STORAGE
        storage_client = storage.Client(project=PROJECT_NAME)

        # OBTENER BUCKET
        bucket = storage_client.bucket(BUCKET_NAME)

        # CONVERTIR DATAFRAME A CSV CON CODIFICACION UTF-8
        archivo_csv = dataframe.to_csv(
            index=False,
            sep="|"
        )

        # CODIFICAR EL ARCHIVO EN UTF-8 CON BOM
        archivo_csv = archivo_csv.encode("utf-8-sig")

        # SUBIR ARCHIVO
        blob = bucket.blob(nombre_archivo_remoto)

        blob.upload_from_string(
            archivo_csv,
            content_type="text/csv; charset=utf-8"
        )

        print(
            f"Archivo '{nombre_archivo_remoto}' subido exitosamente a Google Cloud Storage."
        )

        return nombre_archivo_remoto

    except Exception:
        logging.exception(
            "Error al subir el archivo a Google Cloud Storage."
        )
        return None


# DEFINIR FUNCIÓN PARA VERIFICAR CONEXIÓN A GOOGLE CLOUD STORAGE
def verificar_conexion_google_cloud_storage():

    try:
        # VALIDAR VARIABLES DE ENTORNO
        if not PROJECT_NAME or not BUCKET_NAME:
            raise ValueError(
                "No se encontraron PROJECT_NAME o BUCKET_NAME."
            )

        # CREAR CLIENTE DE GOOGLE CLOUD STORAGE
        storage_client = storage.Client(project=PROJECT_NAME)

        # OBTENER BUCKET
        bucket = storage_client.bucket(BUCKET_NAME)

        # VERIFICAR EXISTENCIA DEL BUCKET
        if bucket.exists():
            print("Conexión exitosa con Google Cloud Storage.")
            print(f"Bucket encontrado: {bucket.name}")
            return True

        else:
            print("No se encontró el bucket.")
            return False

    except Exception:
        logging.exception("Error de conexión con Google Cloud Storage.")
        return False


# VERIFICAR CONEXIÓN AL EJECUTAR ESTE ARCHIVO DIRECTAMENTE
if __name__ == "__main__":
    verificar_conexion_google_cloud_storage()
