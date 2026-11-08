# LIBRERIA PARA AUTENTICACION Y CONEXION A GOOGLE CLOUD STORAGE
from google.cloud import storage
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path

# CARGAR VARIABLES DE ENTORNO
RUTA_ENV = Path(__file__).resolve().parent / ".env"
load_dotenv(RUTA_ENV)


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

        # CREAR CLIENTE DE GOOGLE CLOUD STORAGE
        storage_client = storage.Client(
            project=load_dotenv.get_key(str(RUTA_ENV), "PROJECT_NAME")
        )

        # OBTENER BUCKET
        bucket = storage_client.bucket(
            load_dotenv.get_key(str(RUTA_ENV), "BUCKET_NAME")
        )

        # CONVERTIR DATAFRAME A CSV
        archivo_csv = dataframe.to_csv(
            index=False,
            # encoding="utf-8",
            sep="|"
        )

        # SUBIR ARCHIVO
        blob = bucket.blob(nombre_archivo_remoto)

        blob.upload_from_string(
            archivo_csv,
            content_type="text/csv"
        )

        print(
            f"Archivo '{nombre_archivo_remoto}' subido exitosamente a Google Cloud Storage."
        )

        return nombre_archivo_remoto

    except Exception as e:
        print(f"Error al subir el archivo: {e}")
        return None


# DEFINIR FUNCIÓN PARA VERIFICAR CONEXIÓN A GOOGLE CLOUD STORAGE
def verificar_conexion_google_cloud_storage():

    try:
        # CREAR CLIENTE DE GOOGLE CLOUD STORAGE
        storage_client = storage.Client(
            project=load_dotenv.get_key(str(RUTA_ENV), "PROJECT_NAME")
        )

        # OBTENER BUCKET
        bucket = storage_client.bucket(
            load_dotenv.get_key(str(RUTA_ENV), "BUCKET_NAME")
        )

        # VERIFICAR EXISTENCIA DEL BUCKET
        if bucket.exists():
            print("Conexión exitosa con Google Cloud Storage.")
            print(f"Bucket encontrado: {bucket.name}")
            return True

        else:
            print("No se encontró el bucket.")
            return False

    except Exception as e:
        print(f"Error de conexión: {e}")
        return False


# VERIFICAR CONEXIÓN AL EJECUTAR ESTE ARCHIVO DIRECTAMENTE
if __name__ == "__main__":
    verificar_conexion_google_cloud_storage()
