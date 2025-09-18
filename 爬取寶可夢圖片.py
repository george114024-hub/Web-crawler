import requests
from bs4 import BeautifulSoup
import os

# 專案說明：用於爬取 Pokemon 圖鑑網站的圖片，並儲存至本地。
# 爬取範圍從編號 1 到 1025。
# 注意：若網路連線不穩或網址不存在，程式可能會報錯。

# 定義本地儲存圖片的目錄名稱
LOCAL_PATH = 'pokemon'

# 確保本地目錄存在，如果不存在則創建它
if not os.path.exists(LOCAL_PATH):
    os.makedirs(LOCAL_PATH)

# --- 核心爬蟲迴圈 ---
# 遍歷寶可夢編號 1 到 1025
for i in range(1, 1026):
    
    # 將數字編號格式化為四位數，以符合網址結構
    pokemon_id = f'{i:04}'
    
    # 組合動態的網頁 URL
    url = f'https://tw.portal-pokemon.com/play/pokedex/{pokemon_id}'

    # 第一步：發送 HTTP 請求並解析網頁內容
    try:
        web = requests.get(url, timeout=10) # 設定超時時間，避免程式卡住
        web.raise_for_status() # 如果狀態碼不是 200，則拋出例外
        soup = BeautifulSoup(web.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"無法存取網頁 {url}，錯誤訊息: {e}")
        continue # 跳過本次迴圈，繼續下一個編號
    
    # 第二步：尋找圖片 URL
    # Pokemon 圖鑑網頁的圖片 URL 儲存在 <meta property="og:image"> 標籤中
    img_meta = soup.select('meta[property="og:image"]')
    
    if img_meta:
        img_url = img_meta[0]['content']
        print(f"正在下載編號 {pokemon_id} 的圖片，URL: {img_url}")

        # 第三步：下載並儲存圖片
        try:
            img_file = requests.get(img_url)
            file_path = os.path.join(LOCAL_PATH, f'{pokemon_id}.png')
            
            # 使用 with open() 語法確保檔案在寫入完成後自動關閉
            with open(file_path, 'wb') as f:
                f.write(img_file.content)
            
            print(f"圖片已成功儲存至: {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"下載圖片 {img_url} 時發生錯誤: {e}")
    else:
        print(f"在 {url} 上找不到圖片 URL。")