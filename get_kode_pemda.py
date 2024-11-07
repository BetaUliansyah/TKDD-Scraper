import requests
requests.packages.urllib3.disable_warnings() 
from bs4 import BeautifulSoup
import json
import pandas as pd
from time import perf_counter
start_time = perf_counter()
tahun=2024
s = requests.Session()
provinsi_df = pd.read_csv('kode_provinsi.csv')
kode_provinsi = provinsi_df['kode_provinsi']
pemda_df = pd.DataFrame(columns= ['kode_provinsi', 'nama_provinsi', 'kode_pemda', 'nama_pemda', 'helper'])
for i in kode_provinsi:
    if i == "--":
        continue
    url = f'https://djpk.kemenkeu.go.id/portal/pemda/{i}/{tahun}'
    r = s.get(url, verify=False)
    response_json = json.loads(r.text)
    for j in response_json:
        row_df = pd.DataFrame({'kode_provinsi' : [i],
                               'nama_provinsi' : provinsi_df.loc[provinsi_df['kode_provinsi'] == i, 'nama_provinsi'],
                               'kode_pemda': [j], 
                               'nama_pemda': [response_json[j]],
                               'helper' : str(tahun)+str(i)+str(j)
                              })
        pemda_df = pd.concat([pemda_df, row_df], ignore_index=True)
pemda_df.to_csv('kode_pemda.csv')
end_time = perf_counter()
total_time = end_time - start_time
rows = len(pemda_df)       
print(f"\n---Finished scraping {rows} rows in: {total_time:.2f} seconds---")
