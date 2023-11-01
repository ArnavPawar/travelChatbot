// Get the video element and original video source
//const videoElement = document.getElementById('video');
//const originalVideoSrc = videoElement.children[0].src;
const voiceInputButton = document.getElementById('voice-input-button');
const micButton = document.getElementById('voice-input-button');
const beginButton = document.getElementById('begin-button');
let index=0;
let destionation;
let begin_time;
let end_time;
let number;
let specifications;
//const themeSwitch = document.querySelector('#checkbox');
//const changePersonalityButton = document.getElementById('change-personality-button');
//const viewButton = document.getElementById('view-button');
//const backButton = document.getElementById('back-button');

//let currentAvatar = originalVideoSrc;

// Initialize a new SpeechRecognition object
let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition)();

let personalityIndex = 0;
const personalities = [
"respond to the question in a way of you're the boyfriend who is extra sweet, extra thoughtful, extra playful，extra outgoing, extra brave, extra intelligent, extra empathetic，also always ask a question back",

];
const videoUrls = [
"https://i.imgur.com/msSdHZT.mp4",
];
const googleVoiceNames = [
  "en-US-News-N",  
  "en-US-Wavenet-H",
  "en-US-Standard-B",
  "en-US-Wavenet-H",
  "en-US-Standard-B",
  "en-US-Wavenet-H",
  "en-US-Standard-B",
];


recognition.lang = 'en-US';
recognition.interimResults = false; // We want final results only
recognition.maxAlternatives = 1; // since from 1-10, max 1 is the most accurate

// When recognition successfully transcribes voice input, put it into the text input
recognition.onresult = function(event) {
    document.getElementById('text-input').value = event.results[0][0].transcript;
};

// When the button is clicked, start voice input
voiceInputButton.addEventListener('click', () => {
    recognition.start();
    console.log("listenForVoiceInput function triggered!");
});

// Function to update video source and play it
// Function to update video source and play it


beginButton.addEventListener('click', () => {
    chatHistory.innerHTML = ''; // Clear the chat history
  
    addMessageToChatHistory("Where do you want to travel?", 'bot');
  //  chatHistory.innerHTML = ''; // Clear the chat history
  index=1;
  
  
})

console.log('Script start');


function addMessageToChatHistory(content, sender) {
    const chatHistory = document.getElementById('chat-history');

    const messageDiv = document.createElement('div');
    messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
    messageDiv.textContent = content;

    chatHistory.appendChild(messageDiv);

    // Scroll to the bottom of the chat history
    chatHistory.scrollTop = chatHistory.scrollHeight;
}



// Event handler for button click

document.getElementById('submit-button').addEventListener('click', () => {
    console.log('Button clicked');
  if(index==0){
  	  addMessageToChatHistory("Please click Begin", 'bot');
    return;
  }
    const textInput = document.getElementById('text-input');
  
  	addMessageToChatHistory(textInput.value, 'user');
    console.log('Text to send:', textInput.value);  // <--- HERE
    if(index==1){
      destionation=textInput.value;
  	  addMessageToChatHistory("When does your trip start?", 'bot');
      index++;
  	textInput.value = '';
      
      return;
      
    }
      if(index==2){
        begin_time=textInput.value;
  	  addMessageToChatHistory("When does your trip end?", 'bot');
      index++;
  	textInput.value = '';
        
      return;
      
    }
      if(index==3){
        end_time=textInput.value;
        
  	  addMessageToChatHistory("How many people are there", 'bot');
      index++;
  	textInput.value = '';
        
      return;
      
    }
      if(index==4){
        number=textInput.value;
  	  addMessageToChatHistory("Any other specifications", 'bot');
      index++;
  	textInput.value = '';
        
      return;
      
    }
  if(index==5){
    specifications=textInput.value;
  	textInput.value = '';
    
    //addMessageToChatHistory(destionation, 'bot');
    //addMessageToChatHistory(begin_time, 'bot');
    //addMessageToChatHistory(end_time, 'bot');
    //addMessageToChatHistory(number, 'bot');
    //addMessageToChatHistory(specifications, 'bot');
    //return;

  }
  
   // addMessageToChatHistory("generatedText", 'bot');

    fetch('/chat', { // Change the endpoint to request text
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        text_prompt: textInput.value,
        dest:destionation,
        begin_t:begin_time,
        end_t:end_time,
        number:number,
        specif:specifications,
        extra_prompt: "Limit your answer to be less than 12 words. Always start a new conversation you should always start with 'Hi!'. Can you also ask a related question back?",
    })
      
    
})
.then(response => response.json())
.then(data => {
     // addMessageToChatHistory('generatedText', 'bot');
    const generatedText = data.text;

    // Add the GPT-3 response to the chat history
    addMessageToChatHistory(generatedText, 'bot');
       addMessageToChatHistory("Please click button Begin again to desgin a new trip", 'bot');
})
.catch((error) => {
    console.error('Error:', error);
});
  
  	textInput.value = '';
  index=0;
   
  

    
});






//ICON MIC BUTTON---------------------------------------------------------
// const micButton = document.getElementById('voice-input-button');

// When the button is clicked, start or stop voice input

//-------------------------------------------------------------------------

// Select the theme switch
// const themeSwitch = document.querySelector('#checkbox');

// themeSwitch.addEventListener('change', function(event) {
//   // Check if the switch is "on"
//   if (event.currentTarget.checked) {
//     // Switch to light theme
//     document.body.classList.remove('dark-theme');
//     document.body.classList.add('light-theme');
//   } else {
//     // Switch to dark theme
//     document.body.classList.remove('light-theme');
//     document.body.classList.add('dark-theme');
//   }
// });


const characterNames = [
  "Dave",
  "Rachel",
  "Michael",
  // ... add more character names corresponding to the personalities array
];














// When a new video ends, pause the video instead of restarting it



// Get reference to the text input element
const textInput = document.getElementById('text-input');
// Add 'keydown' event listener to the text input
textInput.addEventListener('keydown', function(event) {
    // If the key pressed was 'Enter' (key code 13)
    if (event.keyCode === 13) {
        // Trigger click event on the submit button
        document.getElementById('submit-button').click();
        
        // Prevent the event from default action (form submission or line break)
        event.preventDefault();
    }
});


//session ID
// Generate a session ID when the page loads
const sessionId = Math.random().toString(36).substr(2);
console.log('Generated session ID:', sessionId);


// clear button
const clearConversationButton = document.getElementById('clear-conversation-button');
const chatHistory = document.getElementById('chat-history');

clearConversationButton.addEventListener('click', () => {
    chatHistory.innerHTML = ''; // Clear the chat history
  index=0;
});
