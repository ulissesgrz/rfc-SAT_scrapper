import sys
import logging
import requests
import datetime
from bs4 import BeautifulSoup

logger = ''

def obtener_data(cfid, rfc):
    url= f"https://siat.sat.gob.mx/app/qr/faces/pages/mobile/validadorqr.jsf?D1=10&D2=1&D3={cfid}_{rfc}"

    response = requests.get(f"{url}")
    soup = BeautifulSoup(response.text.encode('latin-1'), "lxml")
    tables = soup.find_all('table')

    op_dict = dict()
    if len(tables) > 0:
        op_dict['cfid'] = cfid
        op_dict['rfc'] = rfc
        
        # Verificamos si es una empresa
        if len(rfc) == 12:
            denominacion_razon_social = tables[1].find_all('tr')[1].text.strip().split(':')[1]
            regimen_capital = tables[1].find_all('tr')[2].text.strip().split(':')[1]
            fecha_constitucion = tables[1].find_all('tr')[3].text.strip().split(':')[1]
            fecha_inicio_operaciones = tables[1].find_all('tr')[4].text.strip().split(':')[1]
            situacion_contribuyente = tables[1].find_all('tr')[5].text.strip().split(':')[1]
            fecha_ultimo_cambio_situacion = tables[1].find_all('tr')[6].text.strip().split(':')[1]
            
            op_dict['denominacion_razon_social'] = denominacion_razon_social
            op_dict['regimen_capital'] = regimen_capital
            op_dict['fecha_constitucion'] = fecha_constitucion
        
        # Verificamos si es una persona
        if len(rfc) == 13:
            curp = tables[1].find_all('tr')[1].text.strip().split(':')[1]
            nombre = tables[1].find_all('tr')[2].text.strip().split(':')[1]
            apellido_paterno = tables[1].find_all('tr')[3].text.strip().split(':')[1]
            apellido_materno = tables[1].find_all('tr')[4].text.strip().split(':')[1]
            fecha_nacimiento = tables[1].find_all('tr')[5].text.strip().split(':')[1]
            fecha_inicio_operaciones = tables[1].find_all('tr')[6].text.strip().split(':')[1]
            situacion_contribuyente = tables[1].find_all('tr')[7].text.strip().split(':')[1]
            fecha_ultimo_cambio_situacion = tables[1].find_all('tr')[8].text.strip().split(':')[1]
            
            if(len(tables[6].find_all('tr')[4].text.strip()) > 0):
                op_dict['regimen1'] = tables[6].find_all('tr')[4].text.strip().split(':')[1]
            
            if(len(tables[6].find_all('tr')[5].text.strip()) > 0):
                op_dict['fecha_alta1'] = tables[6].find_all('tr')[5].text.strip().split(':')[1]
                
            op_dict['curp'] = curp
            op_dict['nombre'] = nombre
            op_dict['apellido_paterno'] = apellido_paterno
            op_dict['apellido_materno'] = apellido_materno
            op_dict['fecha_nacimiento'] = fecha_nacimiento

        entidad_federativa = tables[4].find_all('tr')[1].text.strip().split(':')[1]
        municipio_delegacion = tables[4].find_all('tr')[2].text.strip().split(':')[1]
        colonia = tables[4].find_all('tr')[3].text.strip().split(':')[1]
        tipo_vialidad = tables[4].find_all('tr')[4].text.strip().split(':')[1]
        nombre_vialidad = tables[4].find_all('tr')[5].text.strip().split(':')[1]
        numero_exterior = tables[4].find_all('tr')[6].text.strip().split(':')[1]
        numero_interior = tables[4].find_all('tr')[7].text.strip().split(':')[1]
        cp = tables[4].find_all('tr')[8].text.strip().split(':')[1]
        correo_electronico = tables[4].find_all('tr')[9].text.strip().split(':')[1]
        al = tables[4].find_all('tr')[10].text.strip().split(':')[1]

        regimen = tables[6].find_all('tr')[2].text.strip().split(':')[1]
        fecha_alta = tables[6].find_all('tr')[3].text.strip().split(':')[1]
        
        op_dict['fecha_inicio_operaciones'] = fecha_inicio_operaciones
        op_dict['situacion_contribuyente'] = situacion_contribuyente
        op_dict['fecha_ultimo_cambio_situacion'] = fecha_ultimo_cambio_situacion

        op_dict['entidad_federativa'] = entidad_federativa
        op_dict['municipio_delegacion'] = municipio_delegacion
        op_dict['colonia'] = colonia
        op_dict['tipo_vialidad'] = tipo_vialidad
        op_dict['nombre_vialidad'] = nombre_vialidad
        op_dict['numero_exterior'] = numero_exterior
        op_dict['numero_interior'] = numero_interior
        op_dict['cp'] = cp
        op_dict['correo_electronico'] = correo_electronico
        op_dict['al'] = al

        op_dict['regimen'] = regimen
        op_dict['fecha_alta'] = fecha_alta

    return op_dict

def inicializar_logger():
    global logger
    logging.basicConfig(filename="scraper.log", format='%(asctime)s [%(levelname)s] %(message)s', filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

if __name__ == "__main__":
    
    inicializar_logger()
    
    ctime = datetime.datetime.now()
    logger.info(f"{ctime} Iniciando proceso.")

    cfid = "15010673331"
    rfc = "UGU450325KY2"
    
    response = obtener_data(cfid, rfc)
    print(response)
    
    ftime = datetime.datetime.now()
    logger.info(f"{ftime} Fin del programa.")
    logger.info(f"{ftime-ctime} Tiempo total.")