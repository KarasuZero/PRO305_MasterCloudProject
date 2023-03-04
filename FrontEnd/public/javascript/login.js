//get forms store username and password
//take username and password and concatinate username + ":" + password
//then base64 encode the string
//save the base64 encoded string to session storage if login is successful return 200

//loginButton on click

var form = document.getElementById("loginForm");
var loginButton = document.getElementById("loginButton");
var username = document.getElementById("username");
var password = document.getElementById("password");


form.addEventListener("submit", function (event) {
    ev.preventDefault();
});






loginButton.addEventListener("click", async () => {
//create user json object to convert to 64 
    var user = {
        operation: "POST_validate_user",
        data: {
        username: username.value.toString(),
        password: password.value.toString()
        }
    };

    console.log("user:" + user);
    var userJSON = JSON.stringify(user);
    console.log(userJSON);
    var user64 = btoa(userJSON);
    console.log("base 64 string "+ user64);
    //auth is = username:password

    console.log("attempting to login...");
   
    await fetch("http://localhost:8010/proxy/register", {
   // xhr.setRequestHeader("Authorization", user64);
   //API KEY - dIT57njCQzasFAKFyBQgQ7CblhmKK9hM9lzGOouY
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Authorization": username.value.toString()
        //"X-Api-Key": "l0EobqYGoD4dCzSTfB99dlDvYjgkOO664JlPmkv5"
    },
    body: user64,
}).then(function (response) {
    if (response.status == 200) {
        console.log("logged in");
        console.log(response);
        //save base64 encoded string to session storage
        //string =  + ":" + password.value.toString();
        sessionStorage.setItem("token", username.value.toString());
        //redirect to home page   
        window.location.href = "http://localhost:3031/home";

    } else {
        console.log("login failed");
        console.log(response);
        //display error message in popup
        alert ("Login failed");
    }

});
});