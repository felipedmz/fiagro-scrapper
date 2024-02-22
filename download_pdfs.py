import requests
import json
from bs4 import BeautifulSoup

file_path = 'sources.txt'
#
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
            print(f"escaping updates...")
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
                        with open(pdf_filename, 'wb') as file:
                            file.write(download.content)
                        print(f"Downloaded {pdf_filename}...")
                    else:
                        print(f"Falha no download de {download_link}. Status={response.status_code}")

