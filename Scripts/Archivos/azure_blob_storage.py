# LIBRERIA DE AZURE BLOB STORAGE
from azure.storage.blob import BlobServiceClient

# MODULO DE CREDENCIALES
from Scripts.Archivos.credencials import obtener_credenciales_azure

# OTRAS LIBRERIAS
import os
import pandas as pd


def subir_datos_a_azure_blob_storage(datos):

    try:
        # VALIDAR QUE SE RECIBA UN DATAFRAME
        if not isinstance(datos, pd.DataFrame):
            raise TypeError(
                "Los datos deben ser un DataFrame de pandas."
            )

        if datos.empty:
            raise ValueError(
                "No hay datos para subir a Azure Blob Storage."
            )

        # OBTENER CREDENCIALES DE AZURE
        credenciales = obtener_credenciales_azure()

        # OBTENER VARIABLES DE ENTORNO
        azure_blob_container_nombre = os.getenv(
            "AZURE_BLOB_CONTAINER_NAME"
        )

        azure_blob_url = os.getenv(
            "AZURE_BLOB_STORAGE_URL"
        )

        # VALIDAR VARIABLES DE ENTORNO
        if not azure_blob_container_nombre or not azure_blob_url:
            raise ValueError(
                "Faltan las variables de entorno de Azure Blob Storage."
            )

        # CREAR CLIENTE DE SERVICIO
        blob_service_client = BlobServiceClient(
            account_url=azure_blob_url,
            credential=credenciales
        )

        # OBTENER CLIENTE DEL CONTENEDOR
        blob_container_client = (
            blob_service_client.get_container_client(
                azure_blob_container_nombre
            )
        )

        # GENERAR NOMBRE DEL ARCHIVO
        nombre_archivo = (
            "apartamentos_habi_"
            f"{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        # CONVERTIR DATAFRAME A CSV EN MEMORIA
        archivo_csv = datos.to_csv(
            index=False,
            encoding="utf-8",
            sep="|"
        )

        # SUBIR ARCHIVO A AZURE BLOB STORAGE
        blob_container_client.upload_blob(
            name=nombre_archivo,
            data=archivo_csv.encode("utf-8"),
            overwrite=False
        )

        print(
            f"Archivo subido correctamente: {nombre_archivo}"
        )

        return nombre_archivo

    except Exception as e:
        print(
            f"Error al subir los datos a Azure Blob Storage: {e}"
        )
        raise
