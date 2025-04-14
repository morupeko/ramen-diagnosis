import pandas as pd

# データの読み込み
df = pd.read_csv('C:\\Users\\admin\\Downloads\\ラーメン店データーベースabout1-500', encoding='shift_jis')

# ラーメンの種類判定の関数（例）
def 判別_ラーメン種類(row):
    if '醤油' in str(row['フィールド5']) or '醤油' in str(row['フィールド3']) or '醤油' in str(row['フィールド4']) or '醤油' in str(row['詳細タイトル1']) or '醤油' in str(row['storeNamePrefix']):
        return '醤油ラーメン'
    elif '味噌' in str(row['フィールド5']) or '味噌' in str(row['フィールド3']) or '味噌' in str(row['フィールド4']) or '味噌' in str(row['詳細タイトル1']) or '醤油' in str(row['storeNamePrefix']):
        return '味噌ラーメン'
    elif '味噌' in str(row['フィールド5']) or 'みそ' in str(row['フィールド3']) or 'みそ' in str(row['フィールド4']) or 'みそ' in str(row['詳細タイトル1']) or '醤油' in str(row['storeNamePrefix']):
        return '味噌ラーメン'    
    elif '塩' in str(row['フィールド5']) or '塩' in str(row['フィールド3']) or '塩' in str(row['フィールド4']) or '塩' in str(row['詳細タイトル1']) or '醤油' in str(row['storeNamePrefix']):
        return '塩ラーメン'
    elif '豚骨' in str(row['フィールド5']) or '豚骨' in str(row['フィールド3']) or '豚骨' in str(row['フィールド4']) or '豚骨' in str(row['詳細タイトル1']) or '醤油' in str(row['storeNamePrefix']):
        return '豚骨ラーメン'
    # その他の判別条件（例）storeNamePrefix
    else:
        return 'その他'

# ラーメンの種類を判別して新しい列に追加
df['ラーメンの種類'] = df.apply(判別_ラーメン種類, axis=1)

# 店名と住所を結合して新しい列に追加
df['店名'] = df['タイトル'] + ' - ' 
df['住所'] = df['フィールド7'] + ' - ' 

# 営業時間と行き方を追加
# 仮にフィールド8が営業時間、フィールド9が行き方だと仮定
df['営業時間'] = '営業時間: ' + df['フィールド8'].fillna('不明')

df['詳細'] = '詳細: ' + df['タイトルリンク'].fillna('不明')
# 結果をCSVとして保存
df[['店名','住所', '営業時間', 'ラーメンの種類','詳細']].to_csv('C:\\Users\\admin\\Downloads\\ラーメン店データーベースabout1-500_hanbetu.csv', index=False, encoding='shift_jis')

# 結果を出力
print(df[['店名','住所', 'ラーメンの種類', '営業時間','詳細']])
