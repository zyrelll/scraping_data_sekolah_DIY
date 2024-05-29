import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import urlparse

# Init URL
urls = [
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040201/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040202/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040203/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040204/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040206/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040207/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040208/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040209/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040210/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040211/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040212/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040213/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040214/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040215/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040216/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040217/3",
    "https://referensi.data.kemdikbud.go.id/pendidikan/dikdas/040218/3",
]

# Init kabupaten
kabupaten = input("Masukkan nama kabupaten: ")

# Init folder
folder_name = "Scraping_Data"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

def scrape_and_save(url):
    # Show URL
    print(f"URL yang dimasukkan: {url}")

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
            rows.append(row)
            
        # Membuat DataFrame dari tabel
        df = pd.DataFrame(rows, columns=headers)
        
        # Membuat nama file dari kabupaten dan kecamatan
        kecamatan = input("Masukkan nama kecamatan: ")
        
        file_name = f"{kabupaten} - {kecamatan}"
        
        # Menyimpan DataFrame ke dalam file Excel
        excel_file = os.path.join(folder_name, f"{file_name}.xlsx")
        df.to_excel(excel_file, index=False, engine='openpyxl')
        
        print("Data berhasil disimpan ke dalam file Excel")
        
    else:
        print(f"Permintaan gagal dengan kode status {response.status_code}")
    
for url in urls:
    scrape_and_save(url)


# # Mengambil semua tag <img>
#     img_tags = soup.find_all('img')
#     for img in img_tags:
#         img_url = img.get('src')
        
#         # Menggabungkan URL gambar dengan URL situs
#         img_url = urljoin(url, img_url)
        
#         # Mengirim permintaan HTTP GET ke URL gambar
#         img_response = requests.get(img_url)
        
#         if img_response.status_code == 200:
#             # Menyimpan gambar ke dalam folder
#             img_name = os.path.basename(img_url)
#             img_path = os.path.join('images', img_name)
#             with open(img_path, 'wb') as img_file:
#                 img_file.write(img_response.content)
                
#             print(f"Gambar {img_name} berhasil disimpan di {img_path}")
#         else:
#             print(f"Gambar {img_url} gagal diunduh")


    # # Membuat folder untuk menyimpan gambar
    # if not os.path.exists('images'):
    #     os.makedirs('images')