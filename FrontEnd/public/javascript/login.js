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

    var userJSON = JSON.stringify(user);
    var user64 = btoa(userJSON);

    console.log("attempting to login...");
   
    await fetch("https://bt594c8e2e.execute-api.us-west-2.amazonaws.com/fastlane/user", {
   // xhr.setRequestHeader("Authorization", user64);
    method: "POST",
    headers: {
        "Content-Type": "text/plain",
        "Authorization": user64
    },
    body: user64,
}).then(function (response) {
    if (response.status == 200) {
        console.log("logged in");
        //save base64 encoded string to session storage
        string = username.value.toString() + ":" + password.value.toString();
        sessionStorage.setItem("token", string);
        //redirect to home page
        window.location.href = "https://localhost:3031/home";
    } else {
        console.log("login failed");
        //display error message in popup
        alert ("Login failed");
    }

});
});