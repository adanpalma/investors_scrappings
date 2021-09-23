import requests as rq
from bs4 import BeautifulSoup as bs

# ssl.create_default_https_context allow download files
# from a https protocol
# ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.lahipotecaria.com/globalinvestors/covered-bond-program/"
main_url = "https://www.lahipotecaria.com"

# Aqui hacemos un request a la direccion url para obtener el content de la
# pagina

htmlpage = rq.get(url)

if htmlpage.status_code != 200:
    print(f"Error Request status code {htmlpage}")
    exit()

# Aqui pasamos el contenido de la pagina a beatifulsoup
# y extraemos todos los tag "a" que son donde estan los arhivos a descargar

# bspage = bs(htmlpage.content, "html.parser", parse_only=ss("h4"))
bspage = bs(htmlpage.content, "html.parser")
main_tag = "div"
atr = {'class': "SE panel-info"}
h4_tag = "h4"
first_main_tags = bspage.find_all(main_tag, atr)

#TODO: convertir en un metodo que reciba el primer find_all y el se encargue
# de buscar recursivamente el h4 para todos los reportes publicados
# y que sea reusable...
for firsts_tags in first_main_tags:
    seconds_tag = firsts_tags.find("h4")
    if "August, 2021" in seconds_tag:
        print("Agosto fue publicado")
    else:
        print("Agosto no ha sido publicado")


