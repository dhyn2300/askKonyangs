from flask import Flask, render_template, request, jsonify
from openai import OpenAI



app = Flask(__name__)

# OpenAI API 키 설정

# 맞춤형 Assistant ID 설정
# extra_context 파일 읽어오기
with open('extra_context.txt', 'r', encoding='utf-8') as file:
    extra_context = file.read()

def get_response(prompt, assistant_id, extra_context):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": extra_context},
                {"role": "user", "content": prompt}
            ],
            user=assistant_id  # 맞춤형 Assistant ID 사용
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")  # 오류 로그 추가
        return str(e)  # 오류 메시지를 직접 반환

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    print(f"Received question: {question}")  # 로그 추가
    if question:
        answer = get_response(question, assistant_id, extra_context)
        print(f"Generated answer: {answer}")  # 로그 추가
        return jsonify({"answer": answer})
    return jsonify({"error": "No question provided"}), 400

if __name__ == "__main__":
    app.run(debug=True)
