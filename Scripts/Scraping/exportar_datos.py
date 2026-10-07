import pandas as pd
from pathlib import Path
from scraping import scraping


def exportar_datos():

    # EJECUTAR FUNCION DE SCRAPING Y OBTENER LOS DATOS
    datos = scraping()

    # DESEMPAQUETAR LOS DATOS OBTENIDOS
    (
        id_apartamento,
        nombre_apartamento,
        direccion_apartamento,
        ciudad_apartamento,
        precio_apartamento,
        estrato_apartamento,
        antiguedad_apartamento,
        apartamento_remodelado,
        area_apartamento,
        habitaciones_apartamento,
        banios_apartamento,
        garaje_apartamento,
        elevadores_apartamento,
        url_apartamento,
        tipo_inmueble,
        porteria_apartamento,
        zona_lavanderia_apartamento,
        gas_apartamento,
        parqueadero_apartamento,
        fecha_hora_informacion
    ) = datos

    # GENERAR DATAFRAME
    df = pd.DataFrame({
        "ID_Apartamento": id_apartamento,
        "Nombre_Apartamento": nombre_apartamento,
        "Dirección_Apartamento": direccion_apartamento,
        "Ciudad_Apartamento": ciudad_apartamento,
        "Precio_Apartamento": precio_apartamento,
        "Estrato_Apartamento": estrato_apartamento,
        "Antigüedad_Apartamento": antiguedad_apartamento,
        "Apartamento_Remodelado": apartamento_remodelado,
        "Área_Apartamento": area_apartamento,
        "Habitaciones_Apartamento": habitaciones_apartamento,
        "Baños_Apartamento": banios_apartamento,
        "Garaje_Apartamento": garaje_apartamento,
        "Elevadores_Apartamento": elevadores_apartamento,
        "URL_Apartamento": url_apartamento,
        "Tipo_Inmueble_Apartamento": tipo_inmueble,
        "Porteria_Apartamento": porteria_apartamento,
        "Zona_Lavandería_Apartamento": zona_lavanderia_apartamento,
        "Gas_Apartamento": gas_apartamento,
        "Parqueadero_Apartamento": parqueadero_apartamento,
        "Fecha_Informacion": fecha_hora_informacion
    })

    # SE DECLARA LA RUTA DONDE VAN A SER ALMACENADOS LOS DATOS
    ruta_exportar = Path(__file__).resolve().parents[2] / "Raw"

    # GENERAR NOMBRE DEL ARCHIVO CON FECHA Y HORA
    nombre_archivo = "apartamentos_habi_{}.csv".format(pd.Timestamp.now().strftime("%Y%m%d_%H%M%S"))

    # EXPORTAR DATAFRAME A CSV
    df.to_csv(
        ruta_exportar / nombre_archivo,
        index=False,
        encoding="utf-8-sig",
        # COLOCAR POR UN DELIMITADOR POR PUNTO Y COMA
        sep="|"
    )

    return "ARCHIVO CSV EXPORTADO EXITOSAMENTE"


if __name__ == "__main__":
    resultado = exportar_datos()
    print(resultado)