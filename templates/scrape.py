import requests
from bs4 import BeautifulSoup
import pandas as pd

# 商品情報をスクレイピングしてCSVに保存する関数
def scrape_amazon():
    amazon_url = "https://www.amazon.co.jp/s?k=%E3%83%A9%E3%83%BC%E3%83%A1%E3%83%B3&i=stripbooks"  # 例: ラーメンの商品ページ
    response = requests.get(amazon_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 商品リストを取得（必要に応じてセレクターは変更）
    products = soup.select('.s-main-slot .s-result-item')

    product_data = []
    for product in products:
        title = product.select_one('h2 a')
        if title:
            name = title.get_text()
            link = "https://www.amazon.co.jp" + title['href']
            price = product.select_one('.a-price .a-offscreen')
            if price:
                price = price.get_text()
            else:
                price = "価格なし"
            
            product_data.append({
                'name': name,
                'link': link,
                'price': price
            })

    # DataFrameに変換してCSVに保存
    df = pd.DataFrame(product_data)
    df.to_csv('amazon_ramen.csv', index=False, encoding='utf-8-sig')

# 実行
scrape_amazon()
