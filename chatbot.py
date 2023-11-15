import openai

openai.api_key = "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"

model_name = "gpt-3.5-turbo"
past_chats = []

def main():
    """
    Main interaction loop for the chatbot.
    """
    print("Welcome to Chatbot! Type 'quit' to exit.")

    user_input = ""
    while user_input.lower() != "quit":
        user_input = input("You: ")

        if user_input.lower() != "quit":
            response = chat_with_openai(user_input)  # Pass user_input as an argument
            past_chats.append((user_input, response))  # Save the conversation
            print(f"Chatbot: {response}")


def chat_with_openai(prompt):
    # Add user's message to the list of messages
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
    for chat in past_chats:
        messages.append({'role': 'user', 'content': chat[0]})
        messages.append({'role': 'assistant', 'content': chat[1]})

    # Add the current user's message
    messages.append({'role': 'user', 'content': prompt})

    # Get a response from OpenAI
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages
    )

    chatbot_response = response.choices[0].message['content']
    return chatbot_response.strip()


if __name__ == "__main__":
    main()
