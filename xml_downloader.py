import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import re
import aiohttp
import aiofiles
import asyncio
from  logging_etl import log_etl

@log_etl
def delete_tmp_files():
    """
    delete all files from tmp folder
   :return:NONE
    """


    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    try:
        for file in os.listdir('tmp'):
            os.remove(os.path.join('tmp', file))
        logging.info('All files from tmp folder were deleted')
    except Exception as e:
        print(e)
        logging.error(e)

@log_etl
def retrive_xml_files_name(url)->list:
    """scrap url and retrive all 'observationAms' xml files name
    :param url: url of the page with xml files name
    :return: list of xml files name
    """
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
            #Extract district name from url with regex
            pattern = r'observationAms_(.*?)_latest'
            match = re.search(pattern, href)
            if match:
                # The district name is in the first group
                district_name = match.group(1)
                # print('district name:', district_name)
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
async def download_file(file_name):
    """download xml file from url acynccronously and save it in tmp folder
    :param file_name: name of the file to download
    :return: NONE
    """

    temp_url = f"https://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/recent/observationAms_{file_name}_history.xml"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(temp_url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(os.path.join('tmp', os.path.basename(file_name+'.xml')), 'wb') as f:
                        await f.write(await resp.read())
                        print(f"Downloaded {temp_url}")
                        logging.info(f'File {file_name} was downloaded')
    except Exception as e:
        print(e)
        logging.error(e)

def main():
    url='https://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/observation_si/index.html'
    delete_tmp_files()
    files= retrive_xml_files_name(url)
    tasks = [download_file(file) for file in files]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

if __name__ == '__main__':
    main()
