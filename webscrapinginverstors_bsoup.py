import csv
import sqlite3
from datetime import date

import requests as rq
from bs4 import BeautifulSoup as bs

#  allow download files from ssl
# from a https protocol
# ssl._create_default_https_context = ssl._create_unverified_context

lineas_a_imprimir = []
fecha_proceso = date.today()

# TODO: incorparar date.strftime para ver si con el campo formato de fecha en
# la base de datos se arma la estructura de la fecha en formato texto y se
# compara para que la siguiente version del script solo muestre aquellos
# reportes que su ultima publicacion no conincide con la que se espera

try:
	# Abro conexion con sqllite3
	conn = sqlite3.connect("global_investror_publication_db.db")
	conn.row_factory = sqlite3.Row  # esto permite que los registros se obtengan
	# como un dictionary o hash
	cur = conn.cursor()
	cur.execute('SELECT * from reports_parameters')
	reportes_a_procesar = cur.fetchall()
	total_registros = len(reportes_a_procesar)
	
	main_url = "https://www.lahipotecaria.com"
	url_anterior = None
	for idx, registro in enumerate(reportes_a_procesar, start=1):
		# {
		publication_name, report_name, url, main_tag, atr, publicated_month_tag, *others_fields, \
		salir_luego_primer_tag = registro
		
		# como  hay urls iguales se controla que no se haga request mas de 1 vez al mismo link
		if url_anterior == None or url_anterior != url:
			# {
			htmlpage = rq.get(url)
			status_code = htmlpage.status_code  # }
		
		url_anterior = url
		
		print(f"Searching for {publication_name} {report_name} ({idx} de {total_registros})")
		
		if status_code != 200:
			# {
			print(f""" {publication_name} {report_name} -> {url} status_code -> {status_code}""")
			continue
		# }
		
		# TODO: convertir en un metodo reusable para todos los reportes
		
		bspage = bs(htmlpage.content, "html.parser")
		
		first_main_tags = bspage.find_all(main_tag, atr)
		
		for firsts_tags in first_main_tags:
			# {
			#  "Si no hay month tag indica que esa pagina habra que buscar por texto"
			if publicated_month_tag != None:
				seconds_tag = firsts_tags.find(publicated_month_tag)
				estado = seconds_tag.text.strip()
			else:
				# al no tener publicated_month_tag se hace una busqueda por texto
				estado = ""
				for tags in first_main_tags:
					estado += tags.text.strip()
			
			lineas_a_imprimir.append([publication_name, report_name, estado])
			
			if salir_luego_primer_tag == "S":
				break  # }
	
	# }
	
	with open("International_Investments.csv", "w") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow([f"Fecha de Reporte {fecha_proceso.strftime('%B %d,%Y')}"])
		writer.writerow(["Publication Name", "Report Name", "Last Publication Date"])
		writer.writerows(lineas_a_imprimir)

finally:
	cur.close()
	conn.close()
