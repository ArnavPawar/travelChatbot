
const WebSocket = require("ws");
const FormData = require("form-data");
const fetch = require("node-fetch");

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
        if(parsedMsg.type === "Text")
        {

            handleMessageText(parsedMsg);
        }
        if(parsedMsg.type === "restaurant")
        {

            handleMessageRestaurants(parsedMsg);
        }
        if(parsedMsg.type === "hotel")
        {

          handleMessageHotels(parsedMsg);
        }
        return;
    }
    function handleMessageText(parsedMsg) {

console.log("I get input!")
        const departure = parsedMsg.departure;
        const destnation = parsedMsg.destnation;
        const startdate = parsedMsg.startdate;
        const arrivaldate=parsedMsg.arrivaldate;
        const numtraveler=parsedMsg.numtraveler;
        const FormData = require('form-data');
        const formData = new FormData();
        formData.append('destnation', destnation);
        formData.append('departure', departure);
        formData.append('startdate', startdate);
        formData.append('arrivaldate', arrivaldate);
        formData.append('numtraveler', numtraveler);
   const fetch = require('node-fetch');
        fetch('http://127.0.0.1:5000/api/text', {
    method: 'POST',
    body: formData
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
})
.then(data => {
    console.log("enter text---------------------------")
    console.log(data);
    server.clients.forEach((c) => {
              c.send(JSON.stringify(data));
            });
})
.catch(error => {
    console.error('Error:', error);
});

        //console.log("---"+arrivaldate)
        //console.log("---"+numtraveler)


    }
    function handleMessageFlight(parsedMsg) {
        // Extract the username from parsedMsg
        //const departure = parsedMsg.departure;
        /*const destnation = parsedMsg.destnation;
        const startdate = parsedMsg.startdate;
        // Create a FormData object with the username value
        const FormData = require('form-data');
        const formData = new FormData();
        formData.append('destnation', destnation);
        formData.append('departure', departure);
        formData.append('startdate', startdate);
        // Make a POST request to the API endpoint*/
        const formData = new FormData();

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
    function handleMessageHotels(parsedMsg) {
      console.log(parsedMsg);
      // Extract the username from parsedMsg
      const numtraveler = parsedMsg.numtraveler;
      const destnation = parsedMsg.destnation;
      const startdate = parsedMsg.startdate;
      const arrivaldate = parsedMsg.arrivaldate;
      // Create a FormData object with the username value
      const FormData = require('form-data');
      const formData = new FormData();
      formData.append('destnation', destnation);
      formData.append('numtraveler', numtraveler);
      formData.append('startdate', startdate);
      formData.append('arrivaldate', arrivaldate);
      // Make a POST request to the API endpoint
      const fetch = require('node-fetch');
      fetch('http://127.0.0.1:5000/api/hotels', {
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