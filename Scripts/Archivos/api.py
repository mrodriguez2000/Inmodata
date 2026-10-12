# API REST DE INMODATA
from fastapi import FastAPI, HTTPException

# Importar FastAPI para crear la API
from Scripts.Archivos.main import ejecutar_proceso

# Importar logging para registrar eventos y errores
import logging

# CONFIGURACIÓN DE LOGS

# Configurar el registro de eventos de la aplicación
logging.basicConfig(level=logging.INFO)

# Crear el logger de este módulo
logger = logging.getLogger(__name__)


# CREACIÓN DE LA API

app = FastAPI(
    title="InmoData API",
    description=(
        "API para ejecutar el scraping de apartamentos "
        "y almacenar los datos en Azure Blob Storage."
    ),
    version="1.0.0"
)


# ENDPOINT PRINCIPAL

@app.get("/")
def inicio():

    # Informar que la API está disponible
    return {
        "proyecto": "InmoData",
        "estado": "API activa",
        "documentacion": "/docs"
    }


# ENDPOINT DE SALUD

@app.get("/salud")
def verificar_salud():

    # Confirmar que la API puede responder
    # Este endpoint NO ejecuta el scraping
    return {
        "estado": "disponible",
        "mensaje": "La API de InmoData está funcionando."
    }


# ENDPOINT PARA EJECUTAR EL SCRAPING

@app.post("/ejecutar-scraping")
def ejecutar_scraping():

    try:

        # Registrar el inicio del proceso
        logger.info(
            "Iniciando el proceso de scraping de InmoData."
        )

        # Ejecutar scraping, transformación y carga a Azure
        # La función ya existe en tu módulo main.py
        nombre_archivo = ejecutar_proceso()

        # Registrar que el proceso terminó correctamente
        logger.info(
            "Proceso finalizado. Archivo: %s",
            nombre_archivo
        )

        # Devolver la respuesta al cliente de la API
        return {
            "estado": "exitoso",
            "mensaje": (
                "El scraping y la carga a Azure "
                "finalizaron correctamente."
            ),
            "archivo": nombre_archivo
        }

    except Exception:

        # Registrar el error completo en los logs
        logger.exception(
            "Error al ejecutar el proceso de InmoData."
        )

        # Informar al cliente que ocurrió un error
        # sin exponer detalles internos ni credenciales
        raise HTTPException(
            status_code=500,
            detail=(
                "No fue posible completar el proceso "
                "de scraping y almacenamiento."
            )
        )