
# LIBRERIA DE PLAYWRIGHT
from playwright.sync_api import sync_playwright

# IMPORTAR LIBRERIA DE UNION DE URLS
from urllib.parse import urljoin

# IMPORTAR LIBRERIA DE PANDAS
import pandas as pd

# IMPORTAR LIBRERIA DE TIEMPO
import datetime


# FUNCION PARA OBTENER LOS DATOS DE CADA APARTADO DEL APARTAMENTO
def obtener_datos_apartamento(pagina, titulo_apartamento):

    # SE OBTIENE EL DETALLE DE CADA APARTAMENTO
    detalle = pagina.locator(
        "div.detail-item"
    ).filter(
        has=pagina.locator(
            "p.item-title",
            has_text=titulo_apartamento
        )
    )

    # SI NO SE ENCUENTRA EL DATO SE RETORNA NONE
    if detalle.count() == 0:
        return None

    # SE OBTIENE EL TEXTO DEL DETALLE DE CADA APARTAMENTO
    return detalle.first.locator(
        "p.item-description"
    ).inner_text().strip()


# FUNCION PRINCIPAL QUE VA A CONTENER TODO EL SCRAPING
def scraping():

    # CREAMOS LAS LISTAS DONDE SE VAN A ALMACENAR LOS DATOS
    id_apartamento = []
    nombre_apartamento = []
    direccion_apartamento = []
    ciudad_apartamento = []
    precio_apartamento = []
    estrato_apartamento = []
    antiguedad_apartamento = []
    apartamento_remodelado = []
    area_apartamento = []
    habitaciones_apartamento = []
    banios_apartamento = []
    garaje_apartamento = []
    elevadores_apartamento = []
    tipo_inmueble = []
    porteria_apartamento = []
    zona_lavanderia_apartamento = []
    gas_apartamento = []
    parqueadero_apartamento = []
    url_apartamento = []

    # FECHA Y HORA DE OBTENCION DE LA INFORMACION
    fecha_hora_informacion = []

    # CONTADORES PARA EL SEGUIMIENTO DEL PROCESO
    apartamentos_procesados = 0
    apartamentos_con_error = 0

    # INICIAMOS PLAYWRIGHT
    with sync_playwright() as p:

        # INICIAMOS EL NAVEGADOR
        # HEADLESS EN FALSO PARA QUE SE VEA EL NAVEGADOR
        # EN AZURE SE UTILIZA EL MODO HEADLESS POR DEFECTO
        browser = p.chromium.launch()

        try:

            # CREAMOS UN CONTEXTO SIN UN VIEWPORT FIJO
            context = browser.new_context(viewport=None)

            try:

                # URL DE LA PAGINA DONDE VAMOS A OBTENER LA INFORMACION
                url = "https://habi.co/venta-apartamentos"

                # ABRIMOS UNA NUEVA PESTAÑA
                page = context.new_page()

                # IR HACIA LA URL
                page.goto(
                    url,
                    timeout=90000,
                    wait_until="domcontentloaded"
                )

                # SE AÑADE UN TIEMPO DE ESPERA PARA QUE CARGUE LA PAGINA
                page.wait_for_timeout(5000)

                # VERIFICAMOS QUE SE ENCUENTREN LAS TARJETAS
                try:

                    page.wait_for_selector(
                        "ul.properties-cards li.card",
                        timeout=60000
                    )

                except Exception as e:

                    print("ADVERTENCIA: NO SE ENCONTRARON LAS TARJETAS DE APARTAMENTOS.")
                    print(repr(e))

                # ACCEDEMOS A CADA PAGINA DE APARTAMENTOS
                while True:

                    # OBTENEMOS LAS TARJETAS DE CADA APARTAMENTO
                    apartamentos = page.locator(
                        "ul.properties-cards li.card"
                    )

                    cantidad_apartamentos = apartamentos.count()

                    # MOSTRAMOS LA CANTIDAD DE APARTAMENTOS ENCONTRADOS
                    print(
                        "APARTAMENTOS ENCONTRADOS EN LA PAGINA: {}".format(
                            cantidad_apartamentos
                        )
                    )

                    # SI NO HAY APARTAMENTOS, FINALIZAMOS LA PAGINACION
                    if cantidad_apartamentos == 0:
                        print("NO SE ENCONTRARON APARTAMENTOS EN ESTA PAGINA.")
                        break

                    # ACCEDEMOS A CADA APARTAMENTO Y OBTENEMOS LA INFORMACION
                    for i in range(cantidad_apartamentos):

                        # OBTENEMOS LA TARJETA DEL APARTAMENTO
                        apartamento_card = apartamentos.nth(i)

                        # CIUDAD DEL APARTAMENTO
                        ciudad = None

                        try:

                            # OBTENEMOS LA CIUDAD DIRECTAMENTE DESDE LA TARJETA
                            ciudad = apartamento_card.locator(
                                "div.card-city p"
                            ).inner_text().strip()

                        except Exception as e:

                            print("ADVERTENCIA: NO SE PUDO OBTENER LA CIUDAD.")
                            print(repr(e))

                        # OBTENEMOS EL ENLACE DE CADA APARTAMENTO
                        try:

                            enlace = apartamento_card.locator(
                                "a.card-details"
                            ).get_attribute("href")

                        except Exception as e:

                            print("ERROR AL OBTENER EL ENLACE DEL APARTAMENTO.")
                            print(repr(e))
                            apartamentos_con_error += 1
                            continue

                        # VERIFICAMOS QUE EL ENLACE EXISTA
                        if not enlace:
                            print("ERROR: EL APARTAMENTO NO TIENE ENLACE.")
                            apartamentos_con_error += 1
                            continue

                        # UNIMOS LA URL CON LA URL PRINCIPAL
                        urls_apartamento = urljoin(url, enlace)

                        # OBTENEMOS EL ID DEL APARTAMENTO
                        id_actual = urls_apartamento.rstrip("/").split("/")[-1]

                        # SE PROCEDE A ABRIR LA URL DEL APARTAMENTO
                        url_apartamento_page = context.new_page()

                        try:

                            # IR HACIA LA URL DEL APARTAMENTO
                            url_apartamento_page.goto(
                                urls_apartamento,
                                timeout=90000,
                                wait_until="domcontentloaded"
                            )

                            # ESPERAMOS A QUE SE CARGUE EL CONTENIDO
                            url_apartamento_page.wait_for_timeout(2000)

                            # VERIFICAMOS QUE LA PESTAÑA SIGA ABIERTA
                            if url_apartamento_page.is_closed():
                                raise Exception(
                                    "La pestaña del apartamento se cerró."
                                )

                            # HACER SCROLL HACIA ABAJO PARA CARGAR INFORMACION
                            altura_anterior = 0
                            veces_sin_cambio = 0
                            intentos = 0

                            while veces_sin_cambio < 2 and intentos < 20:

                                # VERIFICAMOS QUE LA PESTAÑA SIGA ABIERTA
                                if url_apartamento_page.is_closed():
                                    raise Exception(
                                        "La pestaña se cerró durante el scroll."
                                    )

                                # OBTENEMOS LA ALTURA ACTUAL DE LA PAGINA
                                altura_actual = url_apartamento_page.evaluate(
                                    "document.body.scrollHeight"
                                )

                                # HACEMOS SCROLL HACIA ABAJO
                                url_apartamento_page.evaluate(
                                    "window.scrollTo(0, document.body.scrollHeight)"
                                )

                                # SE AÑADE UN TIEMPO DE ESPERA PARA CARGAR INFORMACION
                                url_apartamento_page.wait_for_timeout(1000)

                                # OBTENEMOS NUEVAMENTE LA ALTURA DE LA PAGINA
                                nueva_altura = url_apartamento_page.evaluate(
                                    "document.body.scrollHeight"
                                )

                                # VERIFICAMOS SI LA PAGINA SIGUE AUMENTANDO
                                if nueva_altura == altura_anterior:
                                    veces_sin_cambio += 1
                                else:
                                    veces_sin_cambio = 0

                                # GUARDAMOS LA NUEVA ALTURA DE LA PAGINA
                                altura_anterior = nueva_altura

                                # AUMENTAMOS EL NUMERO DE INTENTOS
                                intentos += 1

                            # SE OBTIENEN LOS DATOS DEL APARTAMENTO

                            # NOMBRE DEL APARTAMENTO
                            apartamento = None

                            nombres = url_apartamento_page.locator(
                                "h1.header-title"
                            )

                            if nombres.count() > 1:
                                apartamento = nombres.nth(1).inner_text().strip()

                            elif nombres.count() == 1:
                                apartamento = nombres.nth(0).inner_text().strip()

                            # DIRECCION DEL APARTAMENTO
                            direccion = None

                            try:

                                direccion = url_apartamento_page.locator(
                                    "div.header-location h2"
                                ).evaluate(
                                    "(elemento) => elemento.childNodes[0].textContent.trim()"
                                )

                            except Exception:
                                direccion = None

                            # PRECIO DEL APARTAMENTO
                            precio = None

                            try:

                                precio_texto = url_apartamento_page.locator(
                                    "p.current-price"
                                ).first.evaluate(
                                    "(elemento) => Array.from(elemento.childNodes)"
                                    ".find(nodo => nodo.nodeType === Node.TEXT_NODE)"
                                    ".textContent.trim()"
                                )

                                precio = precio_texto

                            except Exception:
                                precio = None

                            # ESTRATO DEL APARTAMENTO
                            estrato = obtener_datos_apartamento(
                                url_apartamento_page,
                                "Estrato"
                            )

                            # ANTIGUEDAD DEL APARTAMENTO
                            antiguedad = obtener_datos_apartamento(
                                url_apartamento_page,
                                "Antiguedad"
                            )

                            # APARTAMENTO REMODELADO
                            remodelado = obtener_datos_apartamento(
                                url_apartamento_page,
                                "Remodelado"
                            )

                            # AREA DEL APARTAMENTO
                            area = obtener_datos_apartamento(
                                url_apartamento_page,
                                "Área"
                            )

                            # HABITACIONES DEL APARTAMENTO
                            habitaciones = obtener_datos_apartamento(
                                url_apartamento_page,
                                "Habitaciones"
                            )

                            # BAÑOS DEL APARTAMENTO
                            banios = obtener_datos_apartamento(
                                url_apartamento_page,
                                "Baños"
                            )

                            # GARAJE DEL APARTAMENTO
                            garaje = obtener_datos_apartamento(
                                url_apartamento_page,
                                "Garajes"
                            )

                            # ELEVADORES DEL APARTAMENTO
                            elevadores = obtener_datos_apartamento(
                                url_apartamento_page,
                                "Elevadores"
                            )

                            # TIPO DE INMUEBLE DEL APARTAMENTO
                            tipo_inmueble_apartamento = obtener_datos_apartamento(
                                url_apartamento_page,
                                "Tipo de inmueble"
                            )

                            # PORTERIA DEL APARTAMENTO
                            porteria = obtener_datos_apartamento(
                                url_apartamento_page,
                                "Porteria"
                            )

                            # ZONA DE LAVANDERIA DEL APARTAMENTO
                            zona_lavanderia = obtener_datos_apartamento(
                                url_apartamento_page,
                                "Zona de Lavanderia"
                            )

                            # GAS DEL APARTAMENTO
                            gas = obtener_datos_apartamento(
                                url_apartamento_page,
                                "Gas"
                            )

                            # PARQUEADERO DEL APARTAMENTO
                            parqueadero = obtener_datos_apartamento(
                                url_apartamento_page,
                                "Parqueadero"
                            )

                            # FECHA Y HORA DE OBTENCION DE LA INFORMACION
                            fecha_hora_actual = datetime.datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            )

                            # MENSAJES DE IMPRESION DE LOS DATOS OBTENIDOS
                            print("---------------------------------------------------------")
                            print("ID DE APARTAMENTO: {}".format(id_actual))
                            print("NOMBRE DE APARTAMENTO: {}".format(apartamento))
                            print("DIRECCIÓN DE APARTAMENTO: {}".format(direccion))
                            print("CIUDAD DEL APARTAMENTO: {}".format(ciudad))
                            print("PRECIO DE APARTAMENTO: {}".format(precio))
                            print("ESTRATO DE APARTAMENTO: {}".format(estrato))
                            print("ANTIGUEDAD DE APARTAMENTO: {}".format(antiguedad))
                            print("APARTAMENTO REMODELADO: {}".format(remodelado))
                            print("AREA DE APARTAMENTO: {}".format(area))
                            print("HABITACIONES DE APARTAMENTO: {}".format(habitaciones))
                            print("BAÑOS DE APARTAMENTO: {}".format(banios))
                            print("GARAJE DE APARTAMENTO: {}".format(garaje))
                            print("ELEVADORES DE APARTAMENTO: {}".format(elevadores))
                            print("URL DE APARTAMENTO: {}".format(urls_apartamento))
                            print("TIPO DE INMUEBLE DE APARTAMENTO: {}".format(
                                tipo_inmueble_apartamento
                            ))
                            print("PORTERIA DE APARTAMENTO: {}".format(porteria))
                            print("ZONA DE LAVANDERIA DE APARTAMENTO: {}".format(
                                zona_lavanderia
                            ))
                            print("GAS DE APARTAMENTO: {}".format(gas))
                            print("PARQUEADERO DE APARTAMENTO: {}".format(parqueadero))
                            print("FECHA Y HORA DE OBTENCIÓN DE LA INFORMACIÓN: {}".format(
                                fecha_hora_actual
                            ))
                            print("---------------------------------------------------------\n")

                            # SE ALMACENAN LOS DATOS EN LAS LISTAS CORRESPONDIENTES
                            id_apartamento.append(id_actual)
                            nombre_apartamento.append(apartamento)
                            direccion_apartamento.append(direccion)
                            ciudad_apartamento.append(ciudad)
                            precio_apartamento.append(precio)
                            estrato_apartamento.append(estrato)
                            antiguedad_apartamento.append(antiguedad)
                            apartamento_remodelado.append(remodelado)
                            area_apartamento.append(area)
                            habitaciones_apartamento.append(habitaciones)
                            banios_apartamento.append(banios)
                            garaje_apartamento.append(garaje)
                            elevadores_apartamento.append(elevadores)
                            url_apartamento.append(urls_apartamento)
                            tipo_inmueble.append(tipo_inmueble_apartamento)
                            porteria_apartamento.append(porteria)
                            zona_lavanderia_apartamento.append(zona_lavanderia)
                            gas_apartamento.append(gas)
                            parqueadero_apartamento.append(parqueadero)
                            fecha_hora_informacion.append(fecha_hora_actual)

                            apartamentos_procesados += 1

                        except Exception as e:

                            # SE REGISTRA EL ERROR Y SE CONTINUA CON EL SIGUIENTE APARTAMENTO
                            print("ERROR AL PROCESAR EL APARTAMENTO:")
                            print("ID: {}".format(id_actual))
                            print("URL: {}".format(urls_apartamento))
                            print("ERROR: {}".format(repr(e)))

                            apartamentos_con_error += 1

                        finally:

                            # SE CIERRA LA PESTAÑA DE FORMA SEGURA
                            try:

                                if not url_apartamento_page.is_closed():
                                    url_apartamento_page.close()

                            except Exception as e:

                                print("ADVERTENCIA: NO SE PUDO CERRAR LA PESTAÑA.")
                                print(repr(e))

                    # OBTENEMOS EL BOTON PARA PASAR A LA SIGUIENTE PAGINA
                    boton_siguiente = page.locator(
                        'button[data-testid="btn-after"]'
                    )

                    # VERIFICAMOS SI EL BOTON SIGUE DISPONIBLE
                    if boton_siguiente.count() == 0:
                        break

                    # VERIFICAMOS SI EL BOTON ESTA DESHABILITADO
                    if boton_siguiente.is_disabled():
                        break

                    # MENSAJE PARA SABER EN QUE PAGINA ESTAMOS
                    print("HACIENDO CLICK EN SIGUIENTE...")

                    # HACEMOS CLICK EN EL BOTON SIGUIENTE
                    try:

                        boton_siguiente.click(timeout=30000)

                        # ESPERAMOS A QUE CARGUE LA SIGUIENTE PAGINA
                        page.wait_for_timeout(2000)

                    except Exception as e:

                        print("ERROR AL PASAR A LA SIGUIENTE PAGINA:")
                        print(repr(e))
                        break

                    # VERIFICAMOS QUE LA PAGINA SIGA ABIERTA
                    if page.is_closed():
                        print("ERROR: LA PAGINA PRINCIPAL SE CERRO.")
                        break

                    # OBTENEMOS NUEVAMENTE LAS TARJETAS DE LA SIGUIENTE PAGINA
                    apartamentos = page.locator(
                        "ul.properties-cards li.card"
                    )

                    # MENSAJE PARA VERIFICAR QUE CAMBIO LA PAGINA
                    print(
                        "NUEVA PAGINA - APARTAMENTOS ENCONTRADOS: {}".format(
                            apartamentos.count()
                        )
                    )

            finally:

                # CERRAMOS EL CONTEXTO DEL NAVEGADOR
                try:
                    context.close()
                except Exception as e:
                    print("ADVERTENCIA AL CERRAR EL CONTEXTO:")
                    print(repr(e))

        finally:

            # CERRAMOS EL NAVEGADOR
            try:
                browser.close()
            except Exception as e:
                print("ADVERTENCIA AL CERRAR EL NAVEGADOR:")
                print(repr(e))

    # RESUMEN FINAL DEL PROCESO
    print("=========================================================")
    print("RESUMEN DEL SCRAPING DE HABI")
    print("APARTAMENTOS PROCESADOS: {}".format(apartamentos_procesados))
    print("APARTAMENTOS CON ERROR: {}".format(apartamentos_con_error))
    print("TOTAL DE REGISTROS OBTENIDOS: {}".format(len(id_apartamento)))
    print("PROCESO DE SCRAPING FINALIZADO")
    print("=========================================================")

    # RETORNAMOS LAS LISTAS CON LOS DATOS DE LOS APARTAMENTOS
    return (
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
    )


if __name__ == "__main__":

    scraping()
