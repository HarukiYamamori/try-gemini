import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# .envファイルの読み込み
load_dotenv()

# API-KEYの設定
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

gemini_pro = genai.GenerativeModel("gemini-1.5-flash",
                                   generation_config={"response_mime_type": "application/json"})


def generate_math_problems_json(genre, difficulty, num_problems):
    prompt = f"数学の問題と解答例を{num_problems}個作成してください。単元は{genre}で、難易度は{difficulty}です。解説は詳細に記載してください。解答は、問題文、解答、解説のキーを持つJSONオブジェクトとして出力してください。"
    print(f"プロンプト：{prompt}")
    response = gemini_pro.generate_content(prompt)
    print(response.text)

    # JSON文字列をPythonの辞書型に変換
    try:
        json_data = json.loads(response.text)
        return json_data
    except json.JSONDecodeError:
        print("JSONパースエラーが発生しました。")
        return None


json_result = generate_math_problems_json("二次関数", "上級", 5)
if json_result:
    cnt = 1
    for problem in json_result:
        print(f"第{cnt}問")
        print(f"問題: {problem['problem']}")
        print(f"解答: {problem['answer']}")
        print(f"解説: {problem['explanation']}\n")
        cnt += 1
