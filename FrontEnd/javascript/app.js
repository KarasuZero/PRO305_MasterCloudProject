const express = require('express');

const app = express();
const port = 3031;


app.use('/css', express.static(__dirname + '/node_modules/bootstrap/dist/css'));


app.listen (port, () => {
    console.log(`Listening on port ${port}`);
});