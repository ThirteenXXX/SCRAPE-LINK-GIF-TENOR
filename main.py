import requests
from bs4 import BeautifulSoup

print("===========================================")
print('BOT SCRAPING LINK GIF TENOR BY Thirteen𝕏')
print("===========================================")
print('@ThirteenX_bot')
print("==============")

# Masukkan URL halaman Tenor
url = input("Masukan Link Pencarian GIF: ")

# Token bot Telegram dan chat ID
telegram_token = '7590799899:AAGWjV76tWQCT7ddebglJ09Iv6AigWhg17E'
chat_id = input("Masukan Chat Id: ")

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

# Simpan hasil dalam file .txt
file_path = 'Link_GIF.txt'
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
    print("File berhasil dikirim ke @ThirteenX_bot Telegram.")
else:
    print(f"Gagal mengirim file. Status code: {response.status_code}")
