import requests
from bs4 import BeautifulSoup

#專案說明：用來爬取並儲存 PTT 八卦版文章標題與連結

# PTT 網址的根目錄，用於組合完整的文章連結
URL_ROOT = 'https://www.ptt.cc'

# --- 函式：爬取並儲存 PTT 八卦版文章標題 ---
def scrape_gossiping_articles():
    """
    此函式用於爬取 PTT 八卦版首頁的文章標題與連結，
    並將結果儲存至一個純文字檔案。
    """
    # 第一步：發送 HTTP 請求並處理年齡驗證
    # PTT 八卦版有年齡限制，必須帶入 'over18' 的 Cookie 才能進入
    response = requests.get(f'{URL_ROOT}/bbs/Gossiping/index.html', cookies={'over18': '1'})
    
    # 設置網頁編碼為 UTF-8，以防止中文字亂碼
    response.encoding = 'utf-8'

    # 第二步：使用 BeautifulSoup 解析 HTML 內容
    soup = BeautifulSoup(response.text, "html.parser")

    # 第三步：尋找所有文章標題的 div 標籤
    # 每個文章標題都位於 <div class="title"> 標籤內
    titles = soup.find_all('div', class_='title')
    
    output = ''
    # 第四步：遍歷所有標題標籤，並提取文章標題與連結
    for title_div in titles:
        # 檢查該 div 標籤內是否有 <a> 標籤，排除已被刪除的文章
        article_link = title_div.find('a')
        if article_link:
            title_text = article_link.get_text()
            # 組合完整的文章連結
            full_url = URL_ROOT + article_link['href']
            # 將標題與連結添加到 output 字串，並換行
            output += f'{title_text}\n{full_url}\n\n'

    print(output)

    # 第五步：將結果寫入純文字文件
    # 使用 'with' 語法確保檔案在寫入完成後自動關閉，避免資源洩漏
    with open('Notebookstest.txt', 'w', encoding='UTF-8') as f:
        f.write(output)

    print('文章標題已成功儲存至: Notebookstest.txt')

# 執行爬蟲函式
if __name__ == '__main__':
    scrape_gossiping_articles()