from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import time
from openai import OpenAI

app = Flask(__name__)

def create_assistant():
    global assistant_id
    if assistant_id == "":
        my_assistant = client.beta.assistants.create(
            instructions="You are a helpful assistant. If asked about math or computing problems, write and run code to answer the question.",
            name="MyQuickstartAssistant",
            model="gpt-3.5-turbo",
            tools=[{"type": "code_interpreter"}],
        )
        assistant_id = my_assistant.id
    else:
        my_assistant = client.beta.assistants.retrieve(assistant_id)
        assistant_id = my_assistant.id
    return my_assistant

def create_thread():
    global thread_id
    if thread_id == "":
        thread = client.beta.threads.create()
        thread_id = thread.id
    else:
        thread = client.beta.threads.retrieve(thread_id)
        thread_id = thread.id

    return thread

def file_search_ky():
    global assistant_id
    client.beta.assistants.update(
        assistant_id,
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": ['vs_UMtRqwvFgWR98aySzyL3AAZ6']}},
    )

assistant_id = "asst_aUkQNBqjwNpAKs0k39oZLGUd"
thread_id = ""

chat_history = [
    {"role": "system", "content": "You are a helpful assistant."},
]

@app.before_request
def initialize():
    app.before_request_funcs[None].remove(initialize)
    create_assistant()
    create_thread()
    file_search_ky()

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    print(f"Received question: {question}")  # 로그 추가
    if question:
        message_params = {"thread_id": thread_id, "role": "user", "content": question}
        thread_message = client.beta.threads.messages.create(**message_params)
        run = client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=assistant_id
        )
        while run.status != "completed":
            time.sleep(0.5)
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        response = client.beta.threads.messages.list(thread_id).data[0]
        for content in response.content:
            if content.type == "text":
                text_content = content.text.value
                break  # Exit the loop once the first text content is found

        print(f"Generated answer: {text_content}")  # 로그 추가
        return jsonify({"answer": text_content})
    return jsonify({"error": "No question provided"}), 400

if __name__ == "__main__":
    app.run(debug=True)