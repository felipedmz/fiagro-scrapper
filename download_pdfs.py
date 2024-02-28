import requests
import json
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
import base64
import codecs

def download_pdfs(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            fiagro_split = url.split('/')
            fiagro_code = fiagro_split[len(fiagro_split)-2] # codigo do fundo
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            #
            pdf_reports = soup.find('div', class_='updates')
            if (pdf_reports == None):
                print(f"WARN: escaping updates for={fiagro_code}")
                continue
            attr = pdf_reports.get('data-options')
            data = json.loads(attr)
            for page_item in data['data']['items']:
                for item in page_item:    
                    if (item['titulo'].find('Gerencial') != -1):
                        date_report = item['date'].replace('/', '-')
                        download_link = item['linkpdf']
                        download = requests.get(download_link)
                        if download.status_code == 200:
                            pdf_filename = f'pdfs/{fiagro_code}_{date_report}.pdf'
                            file = open(pdf_filename, 'wb')
                            content_decoded = base64.b64decode(download.content)
                            file.write(content_decoded)
                            file.close()
                            print(f"Downloaded {pdf_filename}...")
                        else:
                            print(f"Falha no download de {download_link}. Status={response.status_code}")
#
def download_series(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            url = line.strip()
            fiagro_split = url.split('/')
            fiagro_code = fiagro_split[len(fiagro_split)-2] # codigo do fundo
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            #
            series_reports = soup.find('div', class_='flexColumn')
            if (series_reports == None):
                print(f"WARN: escaping updates for={fiagro_code}")
                continue
            attr = series_reports.get('data-options')
            data = json.loads(attr)
            df = None
            for page_item in data['data']['items']:
                for item in page_item:
                    print(item)
                    if (df == None):
                        df = pd.DataFrame(columns=item.keys())
                    df = df.append(item, ignore_index=True)
            csv_filename = f'csvs/{fiagro_code}.csv'
            print(csv_filename)
            print(df)
            exit()
            """
            if (item['titulo'].find('Gerencial') != -1):
                
                download_link = item['linkpdf']
                download = requests.get(download_link)
                if download.status_code == 200:
                    
                    with open(pdf_filename, 'wb') as file:
                        file.write(download.content)
                    print(f"Downloaded {pdf_filename}...")
                else:
                    print(f"Falha no download de {download_link}. Status={response.status_code}")
#"""
now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
print(f'> fiagro.scrapper.download_pdfs - started={now}')
start_time = time.time()
file_path = 'sources.txt'
#
download_pdfs(file_path)
#download_series(file_path)
#
end_time = time.time()
elapsed_time = end_time - start_time
print(f'> end - elapsed time={elapsed_time}')