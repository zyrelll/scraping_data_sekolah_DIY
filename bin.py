

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