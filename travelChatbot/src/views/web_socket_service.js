const WebSocket = require('ws');
// Create a WebSocket server object, binding it to port 3001
const wss = new WebSocket.Server({
    port: 3001,
});
// The server is now listening
module.exports.listen = () => {
    // Listen for client connection events
    // 'client' represents the client's connection socket object
    wss.on('connection', client => {
        console.log('A client has successfully connected...');
        // Listen for the 'message' event on the client's connection object
        // 'msg' is the data sent from the client to the server
        client.on('message', async msg => {
            console.log('The client has sent data to the server: ' + msg);
            // You can send a response back to the client here if needed
            wss.clients.forEach(client => {
                client.send(msg);
            });
        });
    });
};
