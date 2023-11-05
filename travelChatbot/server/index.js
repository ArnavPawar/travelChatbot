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
        // handleMessageAnalysis(msg);
        // return;
        const parsedMsg = JSON.parse(msg);
        console.log("success")
        console.log(parsedMsg.id)
        if(parsedMsg.type === "flights")
        {
            handleMessageFlights();
        }
        return;
    }

    function handleMessageFlights(parsedMsg) {
        // Extract the username from parsedMsg
        const departure = parsedMsg.departure;
        const destation = parsedMsg.destation;
        const date = parsedMsg.date;
        console.log(departure,destation,date)
        // Create a FormData object with the username value
        const formData = new FormData();
        formData.append('departure', username);
        formData.append('destation', username);
        formData.append('date', username);
      
        // Make a POST request to the API endpoint
        fetch('http://127.0.0.1:5000/flights', {
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