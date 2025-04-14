import requests
import pandas as pd

# CSVファイルのパス（適宜変更してください）
csv_file_path = "ラーメンデータ_20250330.csv"

# Geolonia APIのURL
geolonia_api_url = "https://api.geolonia.com/v1/search"

# Geolonia APIのAPIキー（Geoloniaから取得したAPIキーを入力）
api_key = "YOUR_API_KEY"  # ここに自分のAPIキーを入力

# CSVの読み込み
df = pd.read_csv(csv_file_path, encoding="utf-8")  # CSVのエンコーディングを適宜変更

# ジオコーディングした結果を保存するための新しい列を作成
df['latitude'] = None
df['longitude'] = None

# 住所をジオコーディングして緯度経度を追加
for index, row in df.iterrows():
    address = row['住所']  # 住所が保存されている列名に合わせてください

    # Geolonia APIへのリクエスト
    params = {
        "q": address,  # 検索クエリとして住所
        "lang": "ja"  # 日本語で結果を取得
    }

    # ヘッダーにAPIキーを追加
    headers = {
        "Authorization": f"Bearer {api_key}"  # APIキーをヘッダーに含める
    }

    # APIリクエストを送信
    response = requests.get(geolonia_api_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['features']:
            latitude = data['features'][0]['geometry']['coordinates'][1]
            longitude = data['features'][0]['geometry']['coordinates'][0]
            # 緯度経度を新しい列に追加
            df.at[index, 'latitude'] = latitude
            df.at[index, 'longitude'] = longitude
        else:
            print(f"住所 {address} に対する結果が見つかりませんでした。")
    else:
        print(f"APIリクエストに失敗しました: {response.status_code}")

# 結果を新しいCSVファイルに保存
output_filename = "output_with_ラーメンデータ.csv"
df.to_csv(output_filename, index=False, encoding="utf-8")  # エンコーディングをutf-8に設定

print(f"ジオコーディング結果を{output_filename}に保存しました。")
