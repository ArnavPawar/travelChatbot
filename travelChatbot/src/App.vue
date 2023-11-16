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

    <div class="container">
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
  
      <!-- New box on the left labeled "Flights" -->
      <div class="daily-planner">
        <h2>Flights</h2>
        <ul ref="flightPlanner"></ul>
      </div>

      <!-- New box on the right labeled "Restaurants" -->
      <div class="daily-planner">
        <h2>Restaurants</h2>
        <ul ref="restaurantPlanner"></ul>
      </div>

       <div class="daily-planner">
        <h2>Hotels</h2>
        <ul ref="hotelPlanner"></ul>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useWebSocket } from './hooks';
export default {
  setup() {

    const ws = useWebSocket(handleMessage);

    const dailyPlanner = ref(null);
    const flightPlanner = ref(null);
    const restaurantPlanner = ref(null);
    const hotelPlanner = ref(null);
    const hotelMessages = ref([]);
    const flightMessages = ref([]);
    const restaurantMessages = ref([]);
    const packingList = ref(null);

    const updateDailyPlanner = (messageTypes) => {
      const dailyPlannerElement = dailyPlanner.value;
      const flightPlannerElement = flightPlanner.value;
      const restaurantPlannerElement = restaurantPlanner.value;
      const hotelPlannerElement = hotelPlanner.value;
      dailyPlannerElement.innerHTML = "";
      flightPlannerElement.innerHTML = "";
      restaurantPlannerElement.innerHTML = "";
      hotelPlannerElement.innerHTML = "";

      messageTypes.forEach((messageType) => {
        if (messageType === "restaurants") {
          restaurantMessages.value.forEach((restaurant) => {
            const listItem = document.createElement("li");
            listItem.innerText = `Restaurant: ${restaurant.name}, Rating: ${restaurant.rating}, Reviews: ${restaurant.reviews}`;
            dailyPlannerElement.appendChild(listItem);

            // Create clones of listItem for other elements
            const restaurantListItem = listItem.cloneNode(true);
            restaurantPlannerElement.appendChild(restaurantListItem);
          });
        } else if (messageType === "flights") {
          flightMessages.value.forEach((flight) => {
            const listItem = document.createElement("li");
            listItem.innerText = `Flight: Departure from ${flight.departure_airport} at ${flight.departure_time}, Arrival at ${flight.arrival_airport} at ${flight.arrival_time}, Price: ${flight.price}`;
            dailyPlannerElement.appendChild(listItem);

            // Create clones of listItem for other elements
            const flightListItem = listItem.cloneNode(true);
            flightPlannerElement.appendChild(flightListItem);
          });
        } else if (messageType === "hotels") {
          hotelMessages.value.forEach((hotel) => {
            const listItem = document.createElement("li");
              listItem.innerText = `Hotel: ${hotel.hotel_name}`;
              if (hotel.rating !== 'NaN')  {
                listItem.innerText += `, Rating: ${hotel.rating}`
              }
              if (hotel.price !== 'NaN')  {
                listItem.innerText += `, Price: ${hotel.price}`
              }
              if (hotel.total_price !== 'NaN')  {
                listItem.innerText += `, Total Price: ${hotel.total_price}`
              }
              if (hotel.special !== 'NaN')  {
                listItem.innerText += `, Special: ${hotel.special}`
              }
              if (hotel.refundable !== 'NaN')  {
                listItem.innerText += `, Refundable`
              }
              if (hotel.tags !== 'NaN')  {
                listItem.innerText += `, Tags: ${hotel.tags}`
              }
              if (hotel.description !== 'NaN')  {
                listItem.innerText += `\nDescription: ${hotel.description}`
              }

            dailyPlannerElement.appendChild(listItem);
            // Create clones of listItem for other elements
            const hotelListItem = listItem.cloneNode(true);
            hotelPlannerElement.appendChild(hotelListItem);

          });
        }
      });
    };


    function handleMessage(message) {
      const response = JSON.parse(message.data);

      if (response.type === "restaurants") {
        console.log('restaurant message', response.restaurants);
        restaurantMessages.value.push(...response.restaurants);
      }
      if(response.type==="Text"){

        const userMessage = document.createElement("li");
        userMessage.classList.add("user-message");
        userMessage.innerText = "User: " + response.API;
        messages.value.appendChild(userMessage);
      }

      if (response.type === "flights") {
        console.log('flight message', response.flights);
        flightMessages.value.push(...response.flights);
      }

      if (response.type === "hotels") {
        console.log('hotels message', response.hotels);
        hotelMessages.value.push(...response.hotels);
    }

      updateDailyPlanner(["restaurants", "flights", "hotels"]);
    }


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

    
    const questions = ["Start Location? new-york-city-new-york-united-states",
    "Destination? los-angeles-california-united-states",
    "Start Time? 2023-11-28",
    "End Time? 2023-11-30",
    "Number of Traveler?"
    ];
    // const questions = ["new-york-city-new-york-united-states",
    // "los-angeles-california-united-states",
    // "2023-11-28",
    // "2023-11-30",
    // "Number of Traveler?"
    // ];
    const userResponses = ref([]);
    const userInput = ref("");

    // New ref to store user inputs as a list
    const userInputs = ref([]);

    const scrollToBottom = () => {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
    };

    const displayQuestion = () => {
      const message = document.createElement("li");
      message.classList.add("bot-message");
      message.innerText = questions[currentQuestion.value];
      currentQuestion.value++;
      messages.value.appendChild(message);
    };

    const sendMessage = () => {
      const userMessage = document.createElement("li");
      userMessage.classList.add("user-message");
      userMessage.innerText = "User: " + userInput.value;
      messages.value.appendChild(userMessage);

      // Add user input to the list
      userInputs.value.push(userInput.value);

      if (currentQuestion.value < questions.length) {
        userResponses.value.push(userInput.value);
        displayQuestion();
      } else {
        displayFinalOutput();

        // Log user inputs to the console
        console.log('User Inputs:', userInputs.value);

        // Add user inputs to the Packing List
        userInputs.value.forEach((input, index) => {
          const listItem = document.createElement("li");
          listItem.innerText = `Question ${index+1}: ${questions[index]}\nUser's Answer: ${input}`;
          packingList.value.appendChild(listItem);
        });
        
      }

      userInput.value = "";
      scrollToBottom();
    };

    const clearChat = () => {
      messages.value.innerHTML = "";
      currentQuestion.value = 0;
      userResponses.value = [];

      // Clear the list of user inputs
      userInputs.value = [];

      displayQuestion();
      responses.value.innerHTML = "";
      scrollToBottom();
    };

    const handleSendRestaurant = () =>{
      if (ws.readyState===1) {
          ws.send(JSON.stringify({
              type: "restaurant",
              // departure: userInputs[0],
              destnation: userInputs.value[1]
              // startdate: userInputs[2],
              // arrivaldate: userInputs[3],
              // numtraveler: userInputs[4]
          }));
          }
    }
    const handleSendText = () =>{
      if (ws.readyState===1) {
          ws.send(JSON.stringify({
              type: "Text",
              departure: userInputs.value[0],
              destnation: userInputs.value[1],
              startdate: userInputs.value[2],
              arrivaldate: userInputs.value[3],
              numtraveler: userInputs.value[4]
          }));
          }
    }
    const handleSendFlight = () =>{
      if (ws.readyState===1) {
          ws.send(JSON.stringify({
              type: "flight",
              departure: userInputs.value[0],
              destnation: userInputs.value[1],
              startdate: userInputs.value[2]
              // arrivaldate: userInputs[3],
              // numtraveler: userInputs[4]
          }));
          }
    }

    const handleSendHotel = () => {
      if (ws.readyState===1) {
          ws.send(JSON.stringify({
              type: "hotel",
              // departure: userInputs.value[0],
              destnation: userInputs.value[1],
              startdate: userInputs.value[2],
              arrivaldate: userInputs.value[3],
              numtraveler: userInputs.value[4]
          }));
          }

    }

    const displayFinalOutput = () => {
      handleSendText();
      handleSendRestaurant();
      handleSendFlight();
      handleSendHotel();
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
      userInputs,
      handleSendRestaurant,
      handleSendHotel,
      updateDailyPlanner,
      dailyPlanner,
      flightPlanner,
      restaurantPlanner,
      hotelPlanner,
      packingList,
    };
  },
};
</script>

<style>
  body {
    text-align: center;
  }

  .header {
    margin-bottom: 30px;
  }

  .chat-container {
    max-width: 100%;
    margin: 0 auto;
    border: 1px solid #ccc;
    padding: 10px;
    background-color: #f9f9f9;
    text-align: left;
    width: 100%;
    max-width: 1200px;
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
    background-color: #E6E6E6;
  }

  .user-message {
    background-color: #007AFF;
  }

  .user-input {
    width: 80%;
    padding: 5px;
    box-sizing: border-box;
  }

  .input-box {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
  }

  .submit-button, .clear-button {
    padding: 5px 10px;
  }

  .responses {
    margin-top: 20px;
    text-align: left;
  }

  .container {
    display: flex;
    justify-content: space-between;
    margin: 10px;
  }

  .daily-planner,
  .packing-list,
  .flight-planner,
  .restaurant-planner {
    flex: 1;
    height: 400px;
    border: 1px solid #ccc;
    background-color: #f9f9f9;
    overflow-y: auto;
    text-align: left;
    margin: 5px;
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