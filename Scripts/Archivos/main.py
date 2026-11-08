# MODULO DE SCRAPING
from scraping import scraping

# MODULO DE GOOGLE CLOUD STORAGE (DONDE SE SUBEN LOS ARCHIVOS CSV A GCS)
from google_cloud_storage import subir_datos_a_google_cloud_storage

# OTRAS LIBRERIAS
import pandas as pd

# FUNCIÓN PARA CORRER LOS PROCESOS DE SCRAPING Y SUBIDA A GCS
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

    # DEFINIR NOMBRE DEL ARCHIVO
    nombre_archivo = (
        f"apartamentos_habi_"
        f"{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    # SUBIR DATOS A GOOGLE CLOUD STORAGE
    nombre_archivo = subir_datos_a_google_cloud_storage(
        df,
        nombre_archivo
    )

    if nombre_archivo is None:
        raise RuntimeError(
            "No fue posible almacenar el archivo en Google Cloud Storage."
        )

    print(
        f"Proceso finalizado. Archivo almacenado: {nombre_archivo}"
    )

    return nombre_archivo

# EJECUTAR EL PROCESO SI EL SCRIPT ES EJECUTADO DIRECTAMENTE
if __name__ == "__main__":
    ejecutar_proceso()
