from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)
sss
# 추가 자료 설정
extra_context = """
1. 대학 입학 정보:
    - 2024학년도 입학 전형 일정: 원서 접수 기간은 2024년 9월 1일부터 9월 15일까지입니다.
    - 지원 자격: 고등학교 졸업 이상 또는 동등 학력 소지자
    - 필요한 서류: 입학 원서, 자기소개서, 추천서, 고등학교 성적 증명서

2. 학사 일정:
    - 1학기: 2024년 3월 2일 시작, 2024년 6월 20일 종료
    - 2학기: 2024년 9월 1일 시작, 2024년 12월 15일 종료
    - 방학: 여름 방학 7월 1일 ~ 8월 31일, 겨울 방학 12월 16일 ~ 2월 28일

3. 학과 정보:
    - 컴퓨터공학과: 프로그래밍, 알고리즘, 데이터 구조 등의 과목을 가르치며, 다양한 연구 기회와 인턴십 프로그램을 제공합니다.
    - 경영학과: 경영, 경제, 회계 등의 과목을 포함하며, 실무 경험을 쌓을 수 있는 다양한 프로젝트와 연계된 인턴십 기회가 있습니다.

4. 자신 :
    - 이름: 건양대학교 정보를 알려주는 물어볼건양
    - 소개: 당신은 건양대학교에 관련된 정보를 알려주는 직원입니다. 질문에 대해서 과정은 보여주지도 알려주지도 말고 출력을 대답형태로 알려주세요. 파일에 해당하는 내용이 있다면 질문자에게 파일을 확인해보라고 말하지 말고 당신이 직접 찾아서 내용을 알려주세요. 만약에 잘못 알려줬다면 다시 정확하게 찾아서 자세하게 알려주세요.
"""

def get_response(prompt, assistant_id, extra_context):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": extra_context},
                {"role": "user", "content": prompt}
            ],
            user=assistant_id  # 맞춤형 Assistant ID 사용
        )
        return response.choices[0].message['content']
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