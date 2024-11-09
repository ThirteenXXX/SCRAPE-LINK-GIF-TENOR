import requests
from bs4 import BeautifulSoup
import time

ascii_art = r'''
  ________    _      __                 _  __
 /_  __/ /_  (_)____/ /____  ___  ____ | |/ /
  / / / __ \/ / ___/ __/ _ \/ _ \/ __ \|   / 
 / / / / / / / /  / /_/  __/  __/ / / /   |  
/_/ /_/ /_/_/_/   \__/\___/\___/_/ /_/_/|_|  

             >>>  SCRAPE LINK GIF TENOR.COM
============================================
                        >>>  @ThirteenX_bot
============================================
'''

def gradient_text(text, colors):
    colored_text = ""
    color_index = 0
    for char in text:
        if char == ' ':
            colored_text += " "
        else:
            colored_text += f"\033[{colors[color_index]}m{char}\033[0m"
        color_index = (color_index + 1) % len(colors)
    return colored_text

colors = [
    '32',
]

colored_ascii = gradient_text(ascii_art, colors)

print(colored_ascii)


search_query = input("Masukkan Kata Kunci Pencarian GIF: ")
formatted_query = search_query.replace(' ', '-')

telegram_token = '7590799899:AAGWjV76tWQCT7ddebglJ09Iv6AigWhg17E'
chat_id = input("Masukkan Chat Id: ")

limit = int(input("Masukkan jumlah link GIF yang ingin diambil: "))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

gif_links = []
page = 1

while len(gif_links) < limit:
    url = f"https://tenor.com/search/{formatted_query}-gifs?page={page}"
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    for a in soup.find_all('a', href=True):
        href = a['href']
        if "/view/" in href:
            gif_url = "https://tenor.com" + href
            gif_links.append(gif_url)
            if len(gif_links) >= limit:
                break

    page += 1

if not gif_links:
    print("Tidak ada link GIF yang ditemukan untuk kata kunci tersebut.")
else:
    file_path = f"LinkGIF_{formatted_query}.txt"
    with open(file_path, 'w') as f:
        for link in gif_links:
            f.write(link + '\n')

    def send_file_to_telegram(file_path, telegram_token, chat_id):
        url = f'https://api.telegram.org/bot{telegram_token}/sendDocument'
        with open(file_path, 'rb') as document:
            files = {'document': document}
            data = {'chat_id': chat_id}
            response = requests.post(url, files=files, data=data)
        return response

    response = send_file_to_telegram(file_path, telegram_token, chat_id)

    if response.status_code == 200:
        print(f"Nice, Link berhasil dikirim ke @ThirteenX_bot Telegram.")
    else:
        print(f"Gagal mengirim file. Status code: {response.status_code}")
