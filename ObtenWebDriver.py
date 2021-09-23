from selenium import webdriver


def obtenwebdriver() -> webdriver:
    # TODO: Esta clase debe ir creciendo hasta que sea capaz de seleccionar el
    # webdriver dependiendo de la plataforma y explorador default que tenga
    # por lo tanto hay que agregar la logica para regresar un objeto del tipo
    # webdriver de selenium
    return webdriver.Safari()
