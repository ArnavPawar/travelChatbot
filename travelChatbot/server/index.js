
const WebSocket = require("ws");

;((Ws) => {
    const server = new Ws.Server({port:8000});
    const init = () => {
        bindEvent()
    }

    function bindEvent(){
        server.on('open',handleOpen);
        server.on('close',handleClose);
        server.on('error',handleError);
        server.on('connection',handleConnection);
    }

    // function handleOpen(e) {
    //     console.log('WebSocket open',e)
    // }

    function handleOpen(e) {
        console.log('WebSocket open', e);
    }
    

    function handleClose(e) {
        console.log('WebSocket close',e)
    }

    function handleError(e) {
        console.log('WebSocket error',e)
    }

    function handleConnection(ws)
    {
        console.log('WebSocket connection')
        ws.on('message',handleMessage)
        return;
    }

    function handleMessage(msg)
    {
        const parsedMsg = JSON.parse(msg);
        if(parsedMsg.type === "flight")
        {

            handleMessageFlight(parsedMsg);
        }
        if(parsedMsg.type === "restaurant")
        {

            handleMessageRestaurants(parsedMsg);
        }
        return;
    }

    function handleMessageFlight(parsedMsg) {
        // Extract the username from parsedMsg
        const departure = parsedMsg.departure;
        const destnation = parsedMsg.destnation;
        const startdate = parsedMsg.startdate;
        // Create a FormData object with the username value
        const FormData = require('form-data');
        const formData = new FormData();
        formData.append('destnation', destnation);
        formData.append('departure', departure);
        formData.append('startdate', startdate);
        // Make a POST request to the API endpoint
        const fetch = require('node-fetch');
        fetch('http://127.0.0.1:5000/api/flights', {
          method: 'POST',
          body: formData
        })
          .then(response => response.json())
          .then(data => {
            console.log('Response from backend:', data);
            server.clients.forEach((c) => {
              c.send(JSON.stringify(data));
            });
          })
          .catch(error => {
            console.error('Error:', error);
          });
    }

    function handleMessageRestaurants(parsedMsg) {
        // Extract the username from parsedMsg
        const destnation = parsedMsg.destnation;
        // Create a FormData object with the username value
        const FormData = require('form-data');
        const formData = new FormData();
        formData.append('destnation', destnation);
        // Make a POST request to the API endpoint
        const fetch = require('node-fetch');
        fetch('http://127.0.0.1:5000/api/restaurants', {
          method: 'POST',
          body: formData
        })
          .then(response => response.json())
          .then(data => {
            console.log('Response from backend:', data);
            server.clients.forEach((c) => {
              c.send(JSON.stringify(data));
            });
          })
          .catch(error => {
            console.error('Error:', error);
          });
    }
    
    init();
})(WebSocket)