import requests
requests.packages.urllib3.disable_warnings() 
from bs4 import BeautifulSoup
import pandas as pd
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pytz import timezone
start_time = perf_counter()

tahun = 2024
filename = f"data-tkdd-{tahun}-" + datetime.now(timezone('Asia/Jakarta')).strftime("%Y-%m-%d--%H-%M") + ".csv"

# Initialize requests session
s = requests.Session()

# Read kode pemda from CSV
pemda_df = pd.read_csv('kode_pemda.csv')
akun_df = pd.read_csv(f'akun-tkdd-{tahun}.csv')
helper = pemda_df['helper']

# Prepare the DataFrame to store results
akun_list = akun_df['Akun'].values.tolist()
tkddvalues_list = []
for i in akun_list:
    tkddvalues_list.append(i + ' (Anggaran)')
    tkddvalues_list.append(i + ' (Realisasi)')
# Prepare the DataFrame to store results
headers = ['tahun', 'kode_provinsi', 'kode_pemda'] + tkddvalues_list
tkdd_df = pd.DataFrame(columns=headers) # Empty DataFrame, only headers

# Define a function to fetch IDM for a given kode_pemda
def fetch_tkdd(code):
    tahun = code[0:4]
    kode_provinsi = code[4:6]
    kode_pemda = code[6:8]
    url = url = f'https://djpk.kemenkeu.go.id/portal/data/tkdd?tahun={tahun}&provinsi={kode_provinsi}&pemda={kode_pemda}'
    try:
        r = s.get(url, verify=False)
        bsoup = BeautifulSoup(r.text, 'html.parser')
        
        # Parse the response to get tkdd data
        data_dict = {'tahun': tahun, 'kode_provinsi' : kode_provinsi, 'kode_pemda' : kode_pemda}
        for i in akun_list:
            if i not in str(bsoup):
                continue
            tkddvalue = bsoup.find("td", string=i)
            data_dict[i + ' (Anggaran)'] = tkddvalue.findNext('td').text.replace(' M','').replace('.','').replace(',','.')
            data_dict[i + ' (Realisasi)'] = tkddvalue.findNext('td').findNext('td').text.replace(' M','').replace('.','').replace(',','.')
        
        # Append data to DataFrame
        data_tkdd = pd.DataFrame(data_dict)
        return data_tkdd
    except Exception as e:
        print(f"Failed to fetch data for kode_pemda {kode_pemda}: {e}")
        return pd.DataFrame(columns=['kode_pemda'])

# Execute the requests concurrently with a max of 10 connections at a time
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(fetch_tkdd, code): code for code in helper}
    for future in as_completed(futures):
        result_df = future.result()
        tkdd_df = pd.concat([tkdd_df, result_df], ignore_index=True)

# Save the results to CSV
tkdd_df.to_csv(filename, index=False)

# Calculate and print the elapsed time
end_time = perf_counter()
total_time = end_time - start_time
rows = len(tkdd_df)
print(f"\n---Finished scraping {rows} rows in: {total_time:.2f} seconds---")
