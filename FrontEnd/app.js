const express = require('express');
const path = require('path');

const app = express();
const port = 3031;





app.use('/css', express.static(__dirname + '/node_modules/bootstrap/dist/css'));
app.use(express.static(path.join(__dirname, 'public')));

app.listen (port, () => {
    console.log(`Listening on port ${port}`);
});

app.get('/login', (req, res) => {
    //login.html
    res.sendFile(path.join(__dirname, '/public/views/login.html'));
});

app.get('/register', (req, res) => {
    //register.html
    res.sendFile(path.join(__dirname, '/public/views/register.html'));
});


