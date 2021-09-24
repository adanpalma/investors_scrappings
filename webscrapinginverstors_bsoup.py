import sqlite3

import requests as rq
from bs4 import BeautifulSoup as bs

# ssl.create_default_https_context allow download files
# from a https protocol
# ssl._create_default_https_context = ssl._create_unverified_context


try:
    # Abro conexion con sqllite3
    conn = sqlite3.connect("global_investror_publication_db.db")
    conn.row_factory = sqlite3.Row  # esto permite que los registros se obtengan
    # como un dictionary o hash
    cur = conn.cursor()
    cur.execute(
            'SELECT * from reports_parameters'
            )

    main_url = "https://www.lahipotecaria.com"
    url_anterior = None
    for registro in cur.fetchall():
        publication_name = registro['publication_name']
        report_name = registro['report_name']
        url = registro['url_link']
        main_tag = registro['html_tag']
        atr = {"class": registro['tag_attr']}

        # si viene null no se busca con find_all y se # busca por texto
        publicated_month_tag = registro['publicated_month_tag']
        publication_month_searched = "August, 2021"

        # esto se hace porque hay urls iguales para no repetir los requests y
        # mejorar un poco el performance
        if url_anterior == None or url_anterior != url:
            htmlpage = rq.get(url)
            status_code = htmlpage.status_code
        url_anterior = url

        # Si el link da error, el mismo se reporta y se continua con otros
        # reportes
        if status_code != 200:
            print(
                    f""" {publication_name} 
                           {report_name} -> {url} status_code -> {status_code}
                """
                    )
            continue

        # TODO: convertir en un metodo reusable para todos los reportes
        bspage = bs(htmlpage.content, "html.parser")

        first_main_tags = bspage.find_all(main_tag, atr)
        for firsts_tags in first_main_tags:
            "Si no hay month tag indica que esa pagina habra que buscar por texto"
        if publicated_month_tag != None:
            seconds_tag = firsts_tags.find(publicated_month_tag)
            estado = seconds_tag.text.strip()

        else:
            # al no tener publicated_month_tag se hace una busqueda por texto
            estado = ""
            for tags in first_main_tags:
                estado += tags.text.strip()

        print(
                f""" {publication_name} 
{report_name} -> {publication_month_searched if 1 == 0 else ""}: {estado}
               """
                )

finally:
    cur.close()
    conn.close()
