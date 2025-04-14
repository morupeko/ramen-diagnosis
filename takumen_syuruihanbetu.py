import pandas as pd

# ラーメンの種類と対応するキーワード
ramen_keywords = {
    "豚骨ラーメン": ["豚骨", "とんこつ", "白湯", "博多"],
    "味噌ラーメン": ["味噌", "みそ", "赤味噌", "白味噌"],
    "塩ラーメン": ["塩", "しお", "塩味", "あっさり"],
    "醤油ラーメン": ["醤油", "しょうゆ", "濃い", "深み"]
}

# 商品の詳細からラーメンの種類を判別する関数
def determine_ramen_type(details):
    # 小文字に変換して検索しやすくする
    details = details.lower()

    # ラーメンの種類をキーワードでチェック
    for ramen_type, keywords in ramen_keywords.items():
        for keyword in keywords:
            if keyword.lower() in details:  # キーワードが詳細に含まれていれば
                return ramen_type
    
    # キーワードが見つからなかった場合
    return "不明"

# 宅麺データを読み込む（フルパス指定）
try:
    # 既存の宅麺データを読み込む（パスをフルパスに変更）
    df_takumen = pd.read_csv(r"C:\Users\admin\ramen\ラーメン店データーベースabout1-500.csv", encoding="utf-8-sig")
    
    # '簡単な詳細' と '具体的な詳細' の欄を使ってラーメンの種類を判別
    # 両方の欄を結合して判別する（片方が空でも問題ないように）
    df_takumen['ラーメンの種類'] = df_takumen.apply(
        lambda row: determine_ramen_type(str(row['js_cm_readmore']) + ' ' + str(row['詳細タイトル'])), axis=1
    )

    # 結果を新しいCSVファイルに保存
    df_takumen.to_csv("ラーメン店データーベースabout1-500.csv", index=False, encoding="utf-8-sig")

    print("ラーメンの種類を判別した新しいCSVファイル 'takumen_with_ramen_type.csv' が作成されました。")

except FileNotFoundError:
    print("宅麺データファイルが見つかりません。ファイルパスを確認してください。")


output_file_path = r"C:\Users\admin\ramen\ラーメン店データーベースabout1-500_type.csv"
df_takumen.to_csv(output_file_path, index=False, encoding="utf-8-sig")
print(f"結果は {output_file_path} に保存されました。")