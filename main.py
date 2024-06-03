import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import urlparse

# Init URL
urls = []
prefix = "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/04"
kabupaten_code = input("Masukkan Code Kabupaten: ")
counter = int(input("Masukkan Jumlah Kecamatan: "))
postfix = "/3/jf/all/all"

for i in range(1, counter + 1):
    x = str(i).zfill(2)
    temp_url = prefix + kabupaten_code + x + postfix
    urls.append(temp_url)

print(urls)

# Init kabupaten
kabupaten = input("Masukkan nama kabupaten: ")

# Init basefolder
basefolder_name = "scraping_data"
if not os.path.exists(basefolder_name):
    os.makedirs(basefolder_name)

# Init Dikmen folder
dikmen_folder = os.path.join(basefolder_name, "DIKDAS")
if not os.path.exists(dikmen_folder):
    os.makedirs(dikmen_folder)

# Init kabupaten folder within Dikmen
kabupaten_folder = os.path.join(dikmen_folder, kabupaten)
if not os.path.exists(kabupaten_folder):
    os.makedirs(kabupaten_folder)

# List to hold all data
all_data = []

def scrape_and_collect(url, index):
    # Mengirim permintaan HTTP GET ke URL
    response = requests.get(url, verify=False)

    # Memeriksa apakah permintaan berhasil (kode status 200)
    if response.status_code == 200:

        # Mengambil konten halaman web
        html_content = response.text

        # Membuat objek BeautifulSoup dari konten
        soup = BeautifulSoup(html_content, 'html.parser')

        # Mencari tabel berdasarkan id
        table = soup.find('table', id='table1')

        # Mengambil header tabel
        headers = []
        for th in table.find('thead').find_all('th'):
            headers.append(th.text.strip())

        # Mengambil baris data dari tabel
        rows = []
        for tr in table.find('tbody').find_all('tr'):
            cells = tr.find_all('td')
            row = [cell.text.strip() for cell in cells]
            link = cells[1].find('a')['href']  # Mendapatkan link dari kolom NPSN
            row.append(link)  # Menambahkan link ke baris data
            rows.append(row)

        # Membuat DataFrame dari tabel
        df = pd.DataFrame(rows, columns=headers + ['NPSN Link'])

        # Membuat nama file dari kabupaten dan kecamatan
        print(f"No. {index}")
        # Show URL
        print(f"URL yang dimasukkan: {url}")
        kecamatan = input("Masukkan nama kecamatan: ")

        # Add 'Kecamatan' and 'Kabupaten' columns
        df['Kecamatan'] = kecamatan
        df['Kabupaten'] = kabupaten

        # Add DataFrame to all_data list
        all_data.append(df)

    else:
        print(f"Permintaan gagal dengan kode status {response.status_code}")

# Scrape all URLs and collect data
for index, url in enumerate(urls, start=1):
    scrape_and_collect(url, index)

# Concatenate all data into a single DataFrame
final_df = pd.concat(all_data, ignore_index=True)

# Menyimpan DataFrame ke dalam file Excel dengan hyperlink
excel_file = os.path.join(kabupaten_folder, f"{kabupaten}.xlsx")
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    final_df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    for idx, row in final_df.iterrows():
        npsn_cell = worksheet.cell(row=idx + 2, column=2)  # NPSN column is the second column
        link = row['NPSN Link']
        npsn_cell.hyperlink = link
        npsn_cell.value = row['NPSN']
        npsn_cell.style = "Hyperlink"

print("Data berhasil disimpan ke dalam file Excel")
