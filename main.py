import requests
from bs4 import BeautifulSoup

print("===========================================")
print('BOT SCRAPING GIF DARI TENOR BY Thirteen𝕏')
print("===========================================")
print('@ThirteenX_bot')
print("==============")

# Masukkan kata kunci pencarian GIF
search_query = input("Masukkan Kata Kunci Pencarian GIF: ")
formatted_query = search_query.replace(' ', '-')  # Mengganti spasi dengan tanda strip untuk URL

# URL pencarian di Tenor dengan kata kunci yang diformat
url = f"https://tenor.com/search/{formatted_query}-gifs"

# Token bot Telegram dan chat ID
telegram_token = '7590799899:AAGWjV76tWQCT7ddebglJ09Iv6AigWhg17E'
chat_id = input("Masukkan Chat Id: ")

# Buat headers agar permintaan terlihat seperti dari browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Kirim request ke halaman
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Cari semua link GIF dengan format yang diinginkan
gif_links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if "/view/" in href:
        gif_url = "https://tenor.com" + href
        gif_links.append(gif_url)

# Simpan hasil dalam file .txt dengan nama file berdasarkan kata kunci
file_path = f"LinkGIF_{formatted_query}.txt"
with open(file_path, 'w') as f:
    for link in gif_links:
        f.write(link + '\n')

# Fungsi untuk mengirimkan file ke bot Telegram
def send_file_to_telegram(file_path, telegram_token, chat_id):
    url = f'https://api.telegram.org/bot{telegram_token}/sendDocument'
    files = {'document': open(file_path, 'rb')}
    data = {'chat_id': chat_id}
    response = requests.post(url, files=files, data=data)
    files['document'].close()
    return response

# Kirim file .txt ke Telegram
response = send_file_to_telegram(file_path, telegram_token, chat_id)

# Cek apakah file berhasil dikirim
if response.status_code == 200:
    print(f"File '{file_path}' Nice, Link berhasil dikirim ke @ThirteenX_bot Telegram.")
else:
    print(f"Gagal mengirim file. Status code: {response.status_code}")
