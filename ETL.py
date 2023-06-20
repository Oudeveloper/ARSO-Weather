import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
import logging

#setup logging
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def log_etl(func):
    def wrapper(*args, **kwargs):
        logging.info('-----------------------------------')
        logging.info(f'Function {func.__name__} was called at {datetime.now()}')
        logging.info(f'Arguments {args} and {kwargs}')
        return func(*args, **kwargs)
    return wrapper

@log_etl
def delete_tmp_files():
    # delete all files from tmp folder
    try:
        for file in os.listdir('tmp'):
            os.remove(os.path.join('tmp', file))
        logging.info('All files from tmp folder were deleted')
    except Exception as e:
        print(e)
        logging.error(e)
@log_etl
def retrive_xml_files(url):
    # scrap and retrive all 'observationAms' xml files from url and save them to local folder and return list of xml files
    retrive_xml_files=[]
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href= link.get('href')
            if 'observationAms' in href and href.endswith('.xml') and 'observationAms_si' not in href:
                logging.info(f'File {href} was found')
                retrive_xml_files.append(link.get('href'))
    except Exception as e:
        print(e)
        logging.error(e)
    return (retrive_xml_files)

@log_etl
def write_xml_files(retrive_xml_files):
    # download xml files and rename and write them to local folder tmp
    city_names=[]
    #check if there is tmp folder. if not create it
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    for file in retrive_xml_files:
        try:
            response = requests.get('https://meteo.arso.gov.si'+file)
            name = file.split('_')[-2]
            logging.info(f'File {name} was downloaded')
            print(f'File {name}.xml was downloaded')
            city_names.append(name)
            with open(os.path.join('tmp', os.path.basename(name+'.xml')), 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(e)
            logging.error(e)
    return city_names


url='https://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/observation_si/index.html'


delete_tmp_files()
print(write_xml_files(retrive_xml_files(url)))
