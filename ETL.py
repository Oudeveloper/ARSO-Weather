import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import re

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
def retrive_xml_files_name(url)->list:
    # scrap and retrive all 'observationAms' xml files name
    xml_files=[]
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            # check if it is xml file and if it is AMS. exclude observationAms_si
            if 'observationAms' not in href or not href.endswith(
                    '.xml') or 'observationAms_si' in href:
                continue
            logging.info(f'File {href} was found')
            #Extract district name from url
            pattern = r'observationAms_(.*?)_latest'
            match = re.search(pattern, href)
            if match:
                # The district name is in the first group
                district_name = match.group(1)
                print('district name:', district_name)
                logging.info(f'district name: {district_name}')
            else:
                logging.info('No city name found in URL.')
                print('No city name found in URL.')

            xml_files.append(district_name)
    except Exception as e:
        print(e)
        logging.error(e)
    print (xml_files)
    return (xml_files)


@log_etl
def write_xml_files(xml_files_names):
    # download xml files and write them to local folder tmp

    #check if there is tmp folder. if not create it
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    for name in xml_files_names:
        temp_url = f"https://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/recent/observationAms_{name}_history.xml"
        try:
            response = requests.get(temp_url)
            logging.info(f'File {name} was downloaded')
            print(f'File {name}.xml was downloaded')
            with open(os.path.join('tmp', os.path.basename(name+'.xml')), 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(e)
            logging.error(e)



url='https://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/observation_si/index.html'

delete_tmp_files()
files= retrive_xml_files_name(url)
write_xml_files(files)
