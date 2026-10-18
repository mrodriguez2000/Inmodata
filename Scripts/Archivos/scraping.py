# LIBRERIA DE PLAYWRIGHT
from playwright.sync_api import sync_playwright

# IMPORTAR LIBRERIA DE UNION DE URLS
from urllib.parse import urljoin

# IMPORTAR LIBRERIA DE PANDAS
import pandas as pd

# IMPORTAR LIBRERIA DE TIEMPO
import datetime


# FUNCION PRINCIPAL QUE VA A CONTENER TODO EL SCRAPING
def scraping():

    # INICIAMOS PLAYWRIGHT
    with sync_playwright() as p:

        # INICIAMOS EL NAVEGADOR
        # HEADLESS EN FALSO PARA QUE SE VEA EL NAVEGADOR
        browser = p.chromium.launch(
            # headless=False,
            # args=["--start-maximized"]
        )

        # CREAMOS UN CONTEXTO SIN UN VIEWPORT FIJO
        context = browser.new_context(viewport=None)

        # URL DE LA PAGINA DONDE VAMOS A OBTENER LA INFORMACION
        url = "https://habi.co/venta-apartamentos"

        # ABRIMOS UNA NUEVA PESTAÑA
        page = context.new_page()

        # IR HACIA LA URL
        page.goto(url)

        # SE AÑADE UN TIEMPO DE ESPERA PARA QUE CARGUE LA PAGINA
        page.wait_for_timeout(5000)

        # CREAMOS LAS LISTAS DONDE VAMOS A ALMACENAR LOS DATOS DEL APARTAMENTO
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
        
        # TAMBIEN SE VA ALMACENAR EN ESE CASO LA FECHA Y HORA EN QUE SE OBTUVO LA INFORMACION DE CADA APARTAMENTO, CON LA FINALIDAD DE QUE ESA INFORMACIÓN NOS FUNCIONE COMO AUDITORIA DE CUANDO SE OBTUVO LA INFORMACION DE CADA APARTAMENTO, YA QUE LA INFORMACION DE LOS APARTAMENTOS PUEDE CAMBIAR CONSTANTEMENTE
        fecha_hora_informacion = []


        # ACCEDEMOS A CADA PAGINA DE APARTAMENTOS
        while True:

            # OBTENEMOS LAS TARJETAS DE CADA APARTAMENTO
            apartamentos = page.locator(
                "ul.properties-cards li.card"
            )

            # MOSTRAMOS LA CANTIDAD DE APARTAMENTOS ENCONTRADOS
            print(
                "APARTAMENTOS ENCONTRADOS EN LA PAGINA: {}".format(
                    apartamentos.count()
                )
            )

            # ACCEDEMOS A CADA APARTAMENTO Y OBTENEMOS LA INFORMACION
            for i in range(apartamentos.count()):


                # OBTENEMOS LA TARJETA DEL APARTAMENTO
                apartamento_card = apartamentos.nth(i)

                # CIUDAD DEL APARTAMENTO
                ciudad = None

                try:

                    # OBTENEMOS LA CIUDAD DIRECTAMENTE DESDE LA TARJETA DEL APARTAMENTO
                    ciudad = apartamento_card.locator(
                        "div.card-city p"
                    ).inner_text().strip()

                except:
                    ciudad = None

                # OBTENEMOS EL ENLACE DE CADA APARTAMENTO
                enlace = apartamento_card.locator(
                    "a.card-details"
                ).get_attribute("href")

                # ALMACENANDO LA URL EN UNA VARIABLE PARA LUEGO UNIRLA CON LA URL PRINCIPAL
                urls_apartamento = urljoin(url, enlace)

                # SE PROCEDE A ABRIR CADA URL DE CADA APARTAMENTO
                url_apartamento_page = context.new_page()

                # IR HACIA LA URL DEL APARTAMENTO
                try:
                    url_apartamento_page.goto(
                        urls_apartamento,
                        timeout=90000,
                        wait_until="domcontentloaded"
                    )
                except Exception as e:
                    print("ERROR AL CARGAR EL APARTAMENTO:")
                    print(urls_apartamento)
                    print(e)
                    url_apartamento_page.close()
                    continue

                # AÑADIR UN PEQUEÑO TIEMPO DE ESPERA PARA QUE CARGUE LA PAGINA
                url_apartamento_page.wait_for_timeout(2000)

                # HACER SCROLL HACIA ABAJO PARA QUE CARGUE EL RESTO DE LA INFORMACION DEL APARTAMENTO
                altura_anterior = 0
                veces_sin_cambio = 0
                intentos = 0

                while veces_sin_cambio < 2 and intentos < 20:

                    # OBTENEMOS LA ALTURA ACTUAL DE LA PAGINA
                    altura_actual = url_apartamento_page.evaluate(
                        "document.body.scrollHeight"
                    )

                    # HACEMOS SCROLL HACIA ABAJO
                    url_apartamento_page.evaluate(
                        "window.scrollTo(0, document.body.scrollHeight)"
                    )

                    # SE AÑADE UN PEQUEÑO TIEMPO DE ESPERA PARA QUE CARGUE LA INFORMACION
                    url_apartamento_page.wait_for_timeout(1000)

                    # OBTENEMOS NUEVAMENTE LA ALTURA DE LA PAGINA
                    nueva_altura = url_apartamento_page.evaluate(
                        "document.body.scrollHeight"
                    )

                    # VERIFICAMOS SI LA PAGINA SIGUE AUMENTANDO DE TAMAÑO
                    if nueva_altura == altura_anterior:
                        veces_sin_cambio += 1
                    else:
                        veces_sin_cambio = 0

                    # GUARDAMOS LA NUEVA ALTURA DE LA PAGINA
                    altura_anterior = nueva_altura

                    # AUMENTAMOS EL NUMERO DE INTENTOS
                    intentos += 1

                # SE OBTIENEN LOS DATOS DE CADA APARTAMENTO

                # NOMBRE DEL APARTAMENTO
                apartamento = None

                try:

                    # OBTENEMOS LOS H1 QUE TIENEN LA CLASE HEADER-TITLE
                    nombres = url_apartamento_page.locator(
                        "h1.header-title"
                    )

                    # HABI TIENE DOS H1, POR ESO OBTENEMOS EL SEGUNDO
                    if nombres.count() > 1:
                        apartamento = nombres.nth(1).inner_text().strip()

                    elif nombres.count() == 1:
                        apartamento = nombres.nth(0).inner_text().strip()

                except:
                    apartamento = None

                # DIRECCIÓN DEL APARTAMENTO
                direccion = None

                try:

                    direccion = url_apartamento_page.locator(
                        "div.header-location h2"
                    ).evaluate(
                        "(elemento) => elemento.childNodes[0].textContent.trim()"
                    )

                except:
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

                except:
                    precio = None

                # DADO QUE ALGUNOS CAMPOS COMO ESTRATO, ANTIGUEDAD, REMODELADO SE ENCUENTRAN DENTRO DE UNA MISMA SECTION SE VA A GENERAR EN UNA FUNCION PARA OBTENER CADA UNO DE LOS DATOS DE CADA APARTAMENTO

                # NOMBRE DE LA FUNCION PARA OBTENER LOS DATOS DE CADA APARTADO
                def obtener_datos_apartamento(titulo_apartamento):

                    # SE OBTIENE EL DETALLE DE CADA APARTAMENTO
                    # PRIMERO BUSCAMOS CADA ELEMENTO CON LA CLASE DETAIL-ITEM Y LUEGO FILTRAMOS POR EL TITULO DE ESA PROPIEDAD PARA OBTENER EL DETALLE DE CADA APARTAMENTO
                    detalle = url_apartamento_page.locator(
                        "div.detail-item"
                    ).filter(
                        has=url_apartamento_page.locator(
                            "p.item-title",
                            has_text=titulo_apartamento
                        )
                    )

                    # SI NO SE ENCUENTRA EL DATO SE RETORNA NONE
                    if detalle.count() == 0:
                        return None

                    # SE OBTIENE EL TEXTO DEL DETALLE DE CADA APARTAMENTO
                    return detalle.locator(
                        "p.item-description"
                    ).inner_text().strip()

                # LLENAR CADA UNO DE LOS CAMPOS DE CADA APARTAMENTO CON LA FUNCION ANTERIOR EN LAS LISTAS CREADAS ANTERIORMENTE

                # ESTRATO DEL APARTAMENTO
                estrato = obtener_datos_apartamento("Estrato")

                # ANTIGUEDAD DEL APARTAMENTO
                antiguedad = obtener_datos_apartamento("Antiguedad")

                # APARTAMENTO REMODELADO
                remodelado = obtener_datos_apartamento("Remodelado")


                # FUNCION PARA TENER LAS DISTRIBUCIONES DE CADA APARTAMENTO
                def distribuciones_apartamento(titulo_distribucion):

                    # SE OBTIENE EL DETALLE DE CADA APARTAMENTO
                    # PRIMERO BUSCAMOS CADA ELEMENTO CON LA CLASE DETAIL-ITEM Y LUEGO FILTRAMOS POR EL TITULO DE ESA PROPIEDAD PARA OBTENER EL DETALLE DE CADA APARTAMENTO
                    detalle = url_apartamento_page.locator(
                        "div.detail-item"
                    ).filter(
                        has=url_apartamento_page.locator(
                            "p.item-title",
                            has_text=titulo_distribucion
                        )
                    )

                    # SI NO SE ENCUENTRA EL DATO SE RETORNA NONE
                    if detalle.count() == 0:
                        return None

                    # SE OBTIENE EL TEXTO DEL DETALLE DE CADA APARTAMENTO
                    return detalle.locator(
                        "p.item-description"
                    ).inner_text().strip()


                # SE PROCEDE A LLENAR CADA UNO DE LOS CAMPOS DE CADA APARTAMENTO CON LA FUNCION ANTERIOR EN LAS LISTAS CREADAS ANTERIORMENTE

                # AREA DEL APARTAMENTO
                area = distribuciones_apartamento("Área")

                # HABITACIONES DEL APARTAMENTO
                habitaciones = distribuciones_apartamento("Habitaciones")

                # BAÑOS DEL APARTAMENTO
                banios = distribuciones_apartamento("Baños")

                # GARAJE DEL APARTAMENTO
                garaje = distribuciones_apartamento("Garajes")

                # ELEVADORES DEL APARTAMENTO
                elevadores = distribuciones_apartamento("Elevadores")

                # FUNCION PARA OBTENER OTRAS CARACTERISTICAS DE CADA APARTAMENTO
                def otras_caracteristicas_apartamento(titulo_caracteristica):
                    # SE OBTIENE EL DETALLE DE CADA APARTAMENTO
                    # PRIMERO BUSCAMOS CADA ELEMENTO CON LA CLASE DETAIL-ITEM Y LUEGO FILTRAMOS POR EL TITULO DE ESA PROPIEDAD PARA OBTENER EL DETALLE DE CADA APARTAMENTO
                    detalle = url_apartamento_page.locator(
                        "div.detail-item"
                    ).filter(
                        has=url_apartamento_page.locator(
                            "p.item-title",
                            has_text=titulo_caracteristica
                        )
                    )

                    # SI NO SE ENCUENTRA EL DATO SE RETORNA NONE
                    if detalle.count() == 0:
                        return None

                    # SE OBTIENE EL TEXTO DEL DETALLE DE CADA APARTAMENTO
                    return detalle.locator(
                        "p.item-description"
                    ).inner_text().strip()

                # SE PROCEDE A LLENAR CADA UNO DE LOS CAMPOS DE CADA APARTAMENTO CON LA FUNCION ANTERIOR EN LAS LISTAS CREADAS ANTERIORMENTE
                # TIPO DE INMUEBLE DEL APARTAMENTO
                tipo_inmueble_apartamento = otras_caracteristicas_apartamento("Tipo de inmueble")

                # PORTERIA DEL APARTAMENTO
                porteria = otras_caracteristicas_apartamento("Porteria")

                # ZONA DE LAVANDERIA DEL APARTAMENTO
                zona_lavanderia = otras_caracteristicas_apartamento("Zona de Lavanderia")

                # GAS DEL APARTAMENTO
                gas = otras_caracteristicas_apartamento("Gas")

                # PARQUEADERO DEL APARTAMENTO
                parqueadero = otras_caracteristicas_apartamento("Parqueadero")

                # HORA Y FECHA DE OBTENCION DE LA INFORMACION DEL APARTAMENTO
                fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                # MENSAJES DE IMPRESIÓN DE LOS DATOS OBTENIDOS
                print("---------------------------------------------------------")
                print("ID DE APARTAMENTO: {}".format(urls_apartamento.split("/")[-2]))
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
                print("TIPO DE INMUEBLE DE APARTAMENTO: {}".format(tipo_inmueble_apartamento))
                print("PORTERIA DE APARTAMENTO: {}".format(porteria))
                print("ZONA DE LAVANDERIA DE APARTAMENTO: {}".format(zona_lavanderia))
                print("GAS DE APARTAMENTO: {}".format(gas))
                print("PARQUEADERO DE APARTAMENTO: {}".format(parqueadero))
                print("FECHA Y HORA DE OBTENCIÓN DE LA INFORMACIÓN: {}".format(fecha_hora_actual))
                print("---------------------------------------------------------\n")


                # SE PROCEDE A CERRAR LA PESTAÑA DE CADA APARTAMENTO PARA QUE NO SE ABRAN MUCHAS PESTAÑAS
                url_apartamento_page.close()


                # OBTENEMOS LOS DATOS DE CADA APARTAMENTO Y LOS AÑADIMOS A LA LISTA CORRESPONDIENTE

                # ID DE APARTAMENTO
                id_apartamento.append(urls_apartamento.split("/")[-2])

                # APARTAMENTO
                nombre_apartamento.append(apartamento)

                # DIRECCION
                direccion_apartamento.append(direccion)

                # CIUDAD
                ciudad_apartamento.append(ciudad)

                # PRECIO
                precio_apartamento.append(precio)

                # ESTRATO
                estrato_apartamento.append(estrato)

                # ANTIGUEDAD
                antiguedad_apartamento.append(antiguedad)

                # REMODELADO
                apartamento_remodelado.append(remodelado)

                # AREA
                area_apartamento.append(area)

                # HABITACIONES
                habitaciones_apartamento.append(habitaciones)

                # BAÑOS
                banios_apartamento.append(banios)

                # GARAJE
                garaje_apartamento.append(garaje)

                # ELEVADORES
                elevadores_apartamento.append(elevadores)

                # URL
                url_apartamento.append(urls_apartamento)

                # TIPO DE INMUEBLE
                tipo_inmueble.append(tipo_inmueble_apartamento)

                # PORTERIA
                porteria_apartamento.append(porteria)

                # ZONA DE LAVANDERIA
                zona_lavanderia_apartamento.append(zona_lavanderia)

                # GAS
                gas_apartamento.append(gas)

                # PARQUEADERO
                parqueadero_apartamento.append(parqueadero)

                # FECHA Y HORA DE OBTENCION DE LA INFORMACION
                fecha_hora_informacion.append(fecha_hora_actual)

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
            boton_siguiente.click()

            # SE AÑADE UN PEQUEÑO TIEMPO DE ESPERA PARA QUE CARGUE LA SIGUIENTE PAGINA
            page.wait_for_timeout(2000)

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

        browser.close()

        print("PROCESO EXITOSO DE SCRAPING DE INFORMACION DE LA PAGINA WEB HABI.CO")

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