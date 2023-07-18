import openai

# Configure OpenAI
openai.api_key = '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'  

# Chatbot Function
def chat_with_bot(user_input):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=user_input,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )

    return response.choices[0].text.strip()

# Main Loop
while True:
    user_input = input("User: ")

    if user_input.lower() == 'exit':
        break

    bot_response = chat_with_bot(user_input)
    print(f"Chatbot: {bot_response}")
