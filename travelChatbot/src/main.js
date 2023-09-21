import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

// const webSocketService = require('./views/web_socket_service');
// // Start the server-side listening, monitoring client connections
// // Once a client successfully connects, it will listen for the 'message' event on that client
// webSocketService.listen();

// const ws = new WebSocket(webSocketUrl);
// // Listen for the 'open' event
// ws.addEventListener('open', e => {
//     console.log('Connection to the server opened ->', e);
// }, false);
// // Listen for the 'close' event
// ws.addEventListener('close', e => {
//     console.log('Connection to the server closed ->', e);
// }, false);
// // Listen for the 'message' event
// ws.addEventListener('message', e => {
//     console.log('Message from the server ->', e);
// }, false);
// // Listen for the 'error' event
// ws.addEventListener('error', e => {
//     console.log('Connection to the server encountered an error ->', e);
// }, false);





createApp(App).mount('#app')
