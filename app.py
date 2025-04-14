import random
from flask import Flask, request, render_template
import pandas as pd
import datetime
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

# 質問リスト
general_questions = [
    "体疲れてるん？",
    "頭疲れてるん？",
    "今ストレスたまってるん？",
    "自分の人生生きてるか？",
    "腹はめちゃこ減ってるん？",
    "今日は運がよかったか？",
    "今日は楽しい出来事があったんか？"
]

# 固定質問
fixed_questions = [
    "こってりがええんか？それともあっさりがええんか？(こってりがいいなら'はい'あっさりがいいなら'いいえ')",  # こってり・あっさり
    "太麺がええんか？それとも細麺がええんか？(太麺がいいなら'はい'細麺がいいなら'いいえ')"  # 太麺・細麺
]

# 曜日ごとの質問
weekday_questions = {
    0: "今週の始まりやけど元気はあるか？",  # 月曜日
    1: "スープまで飲み干したい気分か？",  # 火曜日
    2: "週末の予定は立てたんか？",  # 水曜日
    3: "今の自分は頑張ってるって言い張れるか？",  # 木曜日
    4: "今週は災難やったか？",  # 金曜日
    5: "今週頑張った自分にご褒美をあげたいと思てるやろー？",  # 土曜日
    6: "明日からまたがんばろな！"  # 日曜日
}

# 距離計算（Haversine 公式）
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # 地球の半径 (km)
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c * 1000  # メートル単位で返す

@app.route("/", methods=["GET"])
def index():
    # 現在の曜日と時間帯を取得
    current_day = datetime.datetime.now().weekday()  # 月曜日は0、日曜日は6
    current_hour = datetime.datetime.now().hour

    # 曜日ごとの質問
    day_question = weekday_questions.get(current_day, "今日は何か楽しいことがあったかー？")

    # 時間帯ごとの質問 (午前: 今日は気分がいい？、今日はやる気がある？ / 午後: 今日は頑張った？、今日は何かに挑戦した？)
    if current_hour < 12:
        time_question = ["今日の気分はいいんか？", "今日なんかに挑戦したい気分なんか？"]  # 午前の質問
    else:
        time_question = ["今日は頑張ったと思えるんか？", "今日は何かに挑戦したんか？"]  # 午後の質問

    # ランダムに残りの質問を3つ選ぶ
    random_questions = random.sample(general_questions, 3)

    # 質問を結合
    questions = fixed_questions + [day_question] + time_question + random_questions

    return render_template("index.html", questions=questions)

@app.route("/result", methods=["POST"])
def result():
    # 質問の回答を取得
    answers = {f"q{i}": request.form.get(f"q{i}") for i in range(len(fixed_questions) + len(general_questions) + 2)}

    # ラーメンの種類を決定
    if answers["q0"] == "はい" or answers["q1"] == "はい":
        ramen_type = "豚骨ラーメン"
    elif answers["q2"] == "はい":
        ramen_type = "味噌ラーメン"
    elif answers["q3"] == "はい":
        ramen_type = "塩ラーメン"
    else:
        ramen_type = "醤油ラーメン"

    # ユーザーの現在地を取得
    lat = request.form.get("lat")
    lng = request.form.get("lng")

    # None チェックとデフォルト値設定
    if lat is None or lng is None:
        return render_template("error.html", message="緯度または経度が正しく送信されていません。")

    try:
        user_lat = float(lat)
        user_lng = float(lng)
    except ValueError:
        return render_template("error.html", message="緯度または経度の形式が正しくありません。")

    # ラーメン店データを読み込む
    try:
        df = pd.read_csv(r"C:\Users\admin\ramen\ラーメン店データーベースabout1-500_type.csv", encoding="utf-8")

    except FileNotFoundError:
        return render_template("error.html", message="ラーメン店データファイルが見つかりません。")

    # 診断結果のラーメン種類に一致する店を絞り込む
    filtered_shops = df[df["ラーメンの種類"] == ramen_type].copy()

    if not filtered_shops.empty:
        # 各店との距離を計算し、新しい列として追加
        filtered_shops["距離"] = filtered_shops.apply(
            lambda row: calculate_distance(user_lat, user_lng, row["緯度"], row["経度"]),
            axis=1
        )

        # 近い順に並べて上位3件を取得
        recommended_shops = filtered_shops.sort_values(by="距離").head(3)

        # 距離をフォーマット（1000m未満ならm単位、1000m以上ならkm単位）
        recommended_shops["距離_表示"] = recommended_shops["距離"].apply(
            lambda d: f"{int(d)}m" if d < 1000 else f"{d/1000:.1f}km"
        )

    else:
        recommended_shops = pd.DataFrame()  # 空のデータフレーム

    # 店がなかった場合、コンビニラーメンをおすすめ
    if recommended_shops.empty:
        recommended_shops = [
            {"店名": "カップヌードル", "住所": "全国のコンビニ", "営業時間": "24時間", "詳細": "https://www.nissin.com/jp/products/cupnoodle/", "距離_表示": "近くのコンビニでGET!"}
        ]
    else:
        recommended_shops = recommended_shops.to_dict(orient="records")

    # 宅麺のCSVファイルを読み込む
    try:
        df_takumen = pd.read_csv("takumen_with_ramen_type.csv", encoding="shift_jis")
    except FileNotFoundError:
        return render_template("error.html", message="宅麺データファイルが見つかりません。")

    # ラーメンの種類で宅麺をフィルタリング
    filtered_takumen = df_takumen[df_takumen["ラーメンの種類"] == ramen_type]

    # 宅麺の上位3件を取得
    # 宅麺のランダム3件を取得
    recommended_takumen = filtered_takumen.sample(n=3).to_dict(orient="records")


    # 結果を返す
    return render_template("result.html", ramen_type=ramen_type, shops=recommended_shops, takumen_products=recommended_takumen, user_lat=user_lat, user_lng=user_lng)

if __name__ == "__main__":
    app.run(debug=True)
