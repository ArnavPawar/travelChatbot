import openai
import requests

# Configure OpenAI
openai.api_key = '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'  
#weather_api_key = '1c223b1c1c544d91831152821231807'

import openai



def chat_with_bot(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can experiment with different engines
        prompt=prompt,
        max_tokens=50  # You can adjust the response length
    )
    return response.choices[0].text.strip()

print("Chatbot: Hello! I'm your friendly chatbot. How can I assist you today?")

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Chatbot: Goodbye!")
        break

    prompt = f"You: {user_input}\nChatbot:"
    bot_response = chat_with_bot(prompt)
    print(f"Chatbot: {bot_response}")