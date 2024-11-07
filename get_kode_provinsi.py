import requests
requests.packages.urllib3.disable_warnings() 
from bs4 import BeautifulSoup
import pandas as pd
from time import perf_counter
start_time = perf_counter()
s = requests.Session()
r = s.get('https://djpk.kemenkeu.go.id/portal/data/tkdd', verify=False)
bsoup = BeautifulSoup(r.text, 'html.parser')
provinsi_select = bsoup.find("select", {"id":"sel_provinsi"})
provinsi_options = provinsi_select.find_all("option")
provinsi_df = pd.DataFrame(columns= ['kode_provinsi', 'nama_provinsi'])
for i in provinsi_options:
    row_df = pd.DataFrame({'kode_provinsi': [i['value']], 'nama_provinsi': [i.text]})
    provinsi_df = pd.concat([provinsi_df, row_df], ignore_index=True)
provinsi_df.to_csv('kode_provinsi.csv')
end_time = perf_counter()
total_time = end_time - start_time
rows = len(provinsi_df)
print(f"\n---Finished scraping {rows} rows in: {total_time:.2f} seconds---")
