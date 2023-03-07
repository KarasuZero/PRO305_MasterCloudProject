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

app.get('/home', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/views/catalog.html'));
});

// app.get('/menu', (req, res) => {
//     res.sendFile(path.join(__dirname, '/public/views/storemenu.html'));
// });

app.get('/cart', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/views/cart.html'));
});

app.get('/manage', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/views/manage.html'));
});

app.get('/manage/editResturant', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/views/editstore.html'));
});

app.get('/home/resturantMenu', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/views/storemenu.html'));
});

app.get('/checkout', (req, res) => {
    res.sendFile(path.join(__dirname, '/public/views/checkout.html'));
});




