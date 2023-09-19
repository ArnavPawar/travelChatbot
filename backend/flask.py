from flask import Flask, request, jsonify
from bardapi import BardCookies
import openai

app = Flask(__name__)

cookie_dict = {
    "__Secure-1PSID": "aQgNOlozJyAYWkoC9wWToeRz3vo2De_qhY4NoQVVKZ1OXqYOTc3BNIh1uFTEBm9geGDwjQ.",
    "__Secure-1PSIDTS": "sidts-CjIBSAxbGfMRLt5hEB833rhgyRhN5T9IS4qiJgIrCRY5Linwuk6mgKD5JOS0UiAMDFKR4xAA",
    # Any cookie values you want to pass to the session object.
}

@app.route('/plan_trip', methods=['POST'])
def plan_trip():
    try:
        data = request.json

        destination = data.get("destination")
        city = data.get("city")
        departure_date = data.get("departure_date")
        return_date = data.get("return_date")
        budget = data.get("budget")
        accommodation = data.get("accommodation")
        activities = data.get("activities")
        people = data.get("people")
        planned = data.get("planned")
        other_info = data.get("other_info")

        bard = BardCookies(cookie_dict=cookie_dict)
        result = bard.get_answer(
            f"Can you plan a trip based on all of these questions and answers: {destination} {city} {departure_date} {return_date} {budget} {accommodation} {activities} {activities} {people} {planned} {other_info}"
            " Also, can you plan this trip in this order: ONLY 1 Daily schedule with links for each activity and an estimated price for the activity for everyone(do not provide more than 1 itinerary on the output), ONE A packing list, after providing a daily activity and packing list provide 10 hotel or Airbnb recommendations for the whole trip with links and lastly 10 recommended restaurant locations for the whole trip based on the given information and location"
        )['contents']

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Configure OpenAI
openai.api_key = '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'

def chat_with_bot(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get("user_input")

        if user_input.lower() == 'exit':
            return jsonify({"bot_response": "Goodbye!"})

        prompt = f"You: {user_input}\nChatbot:"
        bot_response = chat_with_bot(prompt)

        return jsonify({"bot_response": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
