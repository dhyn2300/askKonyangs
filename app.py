from flask import Flask, render_template, request, jsonify
from openai import OpenAI

client = OpenAI(api_key='sk-proj-2EkshLNgOj92jjI8Kk9LT3BlbkFJBezMAm0bBFzHWkLChDhL')

app = Flask(__name__)

# OpenAI API 키 설정

# 맞춤형 Assistant ID 설정
assistant_id = 'vs_UMtRqwvFgWR98aySzyL3AAZ6'  # OpenAI 콘솔에서 생성한 Assistant ID로 대체

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
            user=assistant_id 
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")  
        return str(e) 

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