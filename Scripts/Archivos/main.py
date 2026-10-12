# MODULO DE SCRAPING
from Scripts.Archivos.scraping import scraping
from Scripts.Archivos.azure_blob_storage import subir_datos_a_azure_blob_storage

# OTRAS LIBRERIAS
import pandas as pd


def ejecutar_proceso():

    # EJECUTAR SCRAPING
    print("Iniciando scraping de apartamentos...")

    datos = scraping()

    # DEFINIR NOMBRES DE COLUMNAS
    columnas = [
        "ID_Apartamento",
        "Nombre_Apartamento",
        "Direccion_Apartamento",
        "Ciudad_Apartamento",
        "Precio_Apartamento",
        "Estrato_Apartamento",
        "Antiguedad_Apartamento",
        "Apartamento_Remodelado",
        "Area_Apartamento",
        "Habitaciones",
        "Banios",
        "Garaje",
        "Elevadores",
        "URL",
        "Tipo_Inmueble",
        "Porteria",
        "Zona_Lavanderia",
        "Gas",
        "Parqueadero",
        "fecha_hora_informacion"
    ]

    # VALIDAR ESTRUCTURA DE LOS DATOS
    if len(datos) != len(columnas):
        raise ValueError(
            f"Se esperaban {len(columnas)} listas, "
            f"pero el scraping devolvió {len(datos)}."
        )

    # CONVERTIR LISTAS A DATAFRAME
    df = pd.DataFrame(
        dict(zip(columnas, datos))
    )

    # VALIDAR QUE EXISTAN REGISTROS
    if df.empty:
        raise ValueError(
            "El DataFrame no contiene apartamentos."
        )

    print(
        f"Se obtuvieron {len(df)} apartamentos."
    )

    # SUBIR DATOS A AZURE BLOB STORAGE
    nombre_archivo = subir_datos_a_azure_blob_storage(df)

    print(
        f"Proceso finalizado. Archivo almacenado: {nombre_archivo}"
    )

    return nombre_archivo


if __name__ == "__main__":
    ejecutar_proceso()
