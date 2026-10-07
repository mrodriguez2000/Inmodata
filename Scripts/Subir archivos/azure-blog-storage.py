# LIBRERIA DE AZURE BLOB STORAGE
from azure.storage.blob import BlobServiceClient

# IMPORTAR MODULO DE CREDENCIALS
from credencials import obtener_credenciales_azure

import os

# OBTENER CREDENCIALES DE AZURE
credenciales = obtener_credenciales_azure()

# OBTENER LA UBICACION DEL SCRIPT
ruta_script = os.path.dirname(os.path.abspath(__file__))

# CONSTRUIR LA RUTA HACIA LA CARPETA RAW
ruta_archivos = os.path.join(
    ruta_script,
    "..",
    "..",
    "Raw"
)

# CONVERTIR A RUTA ABSOLUTA
ruta_archivos = os.path.abspath(ruta_archivos)

print("Ruta de los archivos:")
print(ruta_archivos)

# RECORRER LOS ARCHIVOS EN LA CARPETA RAW
for filename in os.listdir(ruta_archivos):

    # VALIDAMOS QUE EL ARCHIVO SEA UN CSV
    if filename.endswith(".csv"):

        print("Archivo encontrado: {}".format(filename))

        # OBTENER LA RUTA COMPLETA DEL ARCHIVO
        ruta_completa = os.path.join(ruta_archivos, filename)

        # IMPRIMIR LA RUTA COMPLETA DEL ARCHIVO
        print("Ruta completa del archivo: {}".format(ruta_completa))

        # SE PROCEDE A GENERAR LOS SCRIPTS PARA SUBIR EL ARCHIVO A AZURE BLOB STORAGE
        azure_blob_container_nombre         =       os.getenv("AZURE_BLOB_CONTAINER_NAME")
        azure_blob_url                      =       os.getenv("AZURE_BLOB_STORAGE_URL")

        # SE CREA UN CLIENTE DE SERVICIO DE BLOB STORAGE
        blob_service_client = BlobServiceClient(
            account_url=azure_blob_url,
            credential=credenciales
        )

        # OBTENER CONTENEDOR CLIENTE DE BLOB STORAGE
        blob_container_client = blob_service_client.get_container_client(azure_blob_container_nombre)

        # SE PROCEDE A SUBIR EL ARCHIVO AL BLOB STORAGE
        with open(ruta_completa, "rb") as data:
            blob_container_client.upload_blob(name=filename, data=data, overwrite=True)
            print("Archivo subido exitosamente: {}".format(filename))

    else:
        print("Archivo ignorado: {}".format(filename))