import requests
requests.packages.urllib3.disable_warnings() 
from bs4 import BeautifulSoup
import pandas as pd
from time import perf_counter
import re
start_time = perf_counter()

tahun=2024 # pilih 2018 ke atas yang ada datanya di web djpk
s = requests.Session()
r = s.get(f'https://djpk.kemenkeu.go.id/portal/data/tkdd?tahun={tahun}&provinsi=--&pemda=--', verify=False)
bsoup = BeautifulSoup(r.text, 'html.parser')
akun_table = bsoup.find("div", {"id":"tbl_data"})
akun_tkdd = akun_table.find_all("td")
headers_list = []
for i in akun_tkdd:
    if len(i.text) == 0 or 'text-right' in str(i) : # ignore yang kosong dan class text-right (ini sudah value angka)
        continue
    headers_list.append(i.text + ' (Anggaran)')
    headers_list.append(i.text + ' (Realisasi)')
akun_df = pd.DataFrame(headers_list, columns=['Akun'])
akun_df.to_csv(f'akun-tkdd-{tahun}.csv')
end_time = perf_counter()
total_time = end_time - start_time
rows = len(headers_list)
print(f"\n---Finished scraping {rows} rows in: {total_time:.2f} seconds---")
