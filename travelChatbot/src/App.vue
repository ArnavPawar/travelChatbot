<template>
  <div>
    <div class="header">
      <img
        src="https://cdn.glitch.global/65ce44cc-ad85-4c7a-b33b-520e8d69ba07/plotka_logo.png?v=1698217756131"
        class="illustration"
        alt="Editor illustration"
        title="Click the image!"
      />
    </div>
    <div class="chat-container" ref="chatContainer">
      <ul class="messages" ref="messages"></ul>
    </div>
    <div class="input-box">
      <input type="text" class="user-input" v-model="userInput" placeholder="Type a message..." @keydown.enter="sendMessage" />
      <button class="submit-button" @click="sendMessage">Submit</button>
      <button class="clear-button" @click="clearChat">Clear Chat</button>
    </div>
    <div class="responses" ref="responses"></div>

    <!-- New box on the right labeled "Packing List" -->
    <div class="packing-list">
      <h2>Packing List</h2>
      <ul ref="packingList"></ul>
    </div>

    <!-- New box on the left labeled "Daily Planner" -->
    <div class="daily-planner">
      <h2>Daily Planner</h2>
      <ul ref="dailyPlanner"></ul>
    </div>
  </div>
</template>

<script>
// import { useWebSocket } from './hooks';
// import { ref } from "vue";
// const ws = useWebSocket(handleMessage);
//     const text = ref("");
//     function handleMessage(e) {
//             // console.log('WebSocket message',e.data)
//             text.value = e.data
//     }
import { ref, onMounted } from "vue";
export default {
  setup() {
    const currentQuestion = ref(0);
    // const questions = [
    //   "Where would you like to go?",
    //   "What city and/or address are you planning on staying?",
    //   "What time of month are you going?",
    //   "How long are you planning on staying?",
    //   "What is your budget range?",
    //   "What are some of your interests?",
    //   "Where would you like to stay?",
    //   "Who and how many people are you staying with?",
    //   "What do you have planned already?",
    //   "Add any other info that you think is important for the trip?"
    // ];
    const questions = ["Where do you want to travel (Get place for restaurants)"];
    const userResponses = ref([]);
    const userInput = ref("");

    const scrollToBottom = () => {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    };

    const displayQuestion = () => {
      const message = document.createElement("li");
      message.classList.add("bot-message");
      message.innerText = "Bot: " + questions[currentQuestion.value];
      currentQuestion.value++;
      messages.value.appendChild(message);
    };

    const sendMessage = () => {
      const userMessage = document.createElement("li");
      userMessage.classList.add("user-message");
      userMessage.innerText = "User: " + userInput.value;
      messages.value.appendChild(userMessage);

      if (currentQuestion.value < questions.length) {
        userResponses.value.push(userInput.value);
        displayQuestion();
      } else {
        displayFinalOutput();
      }

      userInput.value = "";
      scrollToBottom();
    };

    const clearChat = () => {
      messages.value.innerHTML = "";
      currentQuestion.value = 0;
      userResponses.value = [];
      displayQuestion();
      responses.value.innerHTML = "";
      scrollToBottom();
    };

    const displayFinalOutput = () => {
      let finalOutput = "Can you plan a trip based on all of these questions and answers:\n";
      userResponses.value.forEach((response, index) => {
        finalOutput += questions[index] + ": " + response + "\n";
      });
      finalOutput += "Also can you plan this trip in this order: ONLY 1 Daily schedule with links for each activity and an estimated price for the activity for everyone(do not provide more than 1 itinerary on the output), ONE A packing list, after providing a daily activity and packing list provide 10 hotel or Airbnb recommendations for the whole trip with links and lastly 10 recommended restaurant locations for the whole trip based on the given information and location";
      const finalOutputMessage = document.createElement("li");
      finalOutputMessage.innerText = "Bot: " + finalOutput;
      messages.value.appendChild(finalOutputMessage);
    };

    const chatContainer = ref(null);
    const messages = ref(null);
    const responses = ref(null);

    onMounted(() => {
      displayQuestion();
    });

    return {
      currentQuestion,
      questions,
      userResponses,
      userInput,
      sendMessage,
      clearChat,
      chatContainer,
      messages,
      responses,
    };
  },
};
</script>


<style>
        body {
            text-align: center;
        }

        .header {
            margin-bottom: 20px;
        }

        .chat-container {
            max-width: 1000px;
            margin: 0 auto;
            border: 1px solid #ccc;
            padding: 10px;
            background-color: #f9f9f9;
            display: inline-block;
            text-align: left;
            width: 400px;
            height: 400px;
            overflow-y: auto;
        }

        .messages {
            list-style-type: none;
            margin: 0;
            padding: 0;
        }

        .messages li {
            margin-bottom: 10px;
            padding: 5px;
            border-radius: 10px;
        }
        .bot-message {
            background-color: #E6E6E6; /* Light gray for bot's messages */
        }
        .user-message {
            background-color: #007AFF; /* Light green for user's messages */
        }

        .user-input {
            width: calc(100% - 20px); /* Set width to match chat container and subtract padding */
            padding: 5px;
            box-sizing: border-box; /* Include padding in width calculation */
        }

        .input-box {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 10px;
            margin-left: 630px;
            width: 30%; /* Make the input box take full width of the chat container */
        }

        .submit-button, .clear-button {
            padding: 5px 10px;
        }

        .responses {
            margin-top: 20px;
            text-align: left;
        }
        .daily-planner,
        .packing-list {
            width: calc(30% - 20px); /* Adjust width as needed */
            height: 400px;
            border: 1px solid #ccc;
            background-color: #f9f9f9;
            margin: 0 10px;
            overflow-y: auto;
            display: inline-block;
            text-align: left;
        }

        h2 {
            text-align: center;
        }

        ul {
            list-style-type: none;
            padding: 0;
        }

        ul li {
            padding: 5px;
            border-bottom: 1px solid #ccc;
        }
    </style>