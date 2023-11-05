from flask import Blueprint, render_template, request, jsonify

views = Blueprint(__name__, "views")

arnav= "wow thats so cool"

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/", methods=["GET","POST"])
def handle_post_request():

    data = request.get_json()  # Get JSON data from the request
    text_prompt = data.get('text_prompt')  # Extract 'text_prompt' from the JSON data

    print("Received data:", text_prompt)  # Print received data to the terminal
    tripPlan=chat_with_openai(text_prompt)

    return jsonify({"response": "Received data: " + text_prompt, "trip": tripPlan})
# @views.route("/profile/<username>")
# def profile(username):
#     return render_template("index.html",name=username)



import openai
openai.api_key = "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"
model_name = "gpt-3.5-turbo"

def chat_with_openai(prompt):
    # Add user's message to the list of messages
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
    # Add the current user's message
    messages.append({'role': 'user', 'content': prompt})

    # Get a response from OpenAI
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages
    )

    chatbot_response = response.choices[0].message['content']
    return chatbot_response.strip()