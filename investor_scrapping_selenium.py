from ObtenWebDriver import obtenwebdriver

# Este codigo es un ejemplo para randomizar el tiempo de espera entre
# las acciones click de la pagina y evitar que los detectores de robot detecten
# el mismo tiempo de click. Es a manera de ejemplo
# for _ in range(4):
#   try:
#     obten el elemento boton
#     luego haz click  boton.click()
#     sleep(random.uniform(8.0,10.0))
#   except:
#     el except es solo por si el click falla.....
#     break

# Variables
# TODO: publication_name y report_name serian las llaves que deberia usar para
# buscar en la base de datos el reporte que desesamos validar si se publico
# por ahora lo estoy haciendo fijo ya que es una prueba de concepto. Se puede
# crear un programa por cada report
publication_name = "Debt Issuanses"
report_name = "Mortgage Report"
url_publication_name = "https://www.lahipotecaria.com/globalinvestors/covered-bond-program/"

web_driver = obtenwebdriver()  # TODO: Cambiar llamado directo a safari por una clase que obtenga el driver
try:
    web_driver.get(url_publication_name)

    web_driver.maximize_window()
    reportes = web_driver.find_elements_by_xpath(
            '//div[@class="MOD '
            'panel-info"]'
            )
    for elemento in reportes:
        texto = elemento.find_element_by_xpath('.//h4').text
        print(texto)
finally:
    web_driver.close()
