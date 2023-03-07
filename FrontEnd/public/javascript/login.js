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
        sessionStorage.setItem("usernametoken", username.value.toString());
        sessionStorage.setItem("password", password.value.toString());
        //call function with http request to discover if user is a customer or store onwer
        getUserType();

    } else {
        console.log("login failed");
        console.log(response);
        //display error message in popup
        alert ("Login failed");
    }

});
});

//async function to find out if user is a customer or store owner
async function getUserType() {
    let userBody = { "operation": "POST_Return_User_Role",
     "data": { "username": sessionStorage.getItem("usernametoken") } 
    }


    let bodyJSON = JSON.stringify(userBody);
    let body64 = btoa(bodyJSON);
    console.log(body64);
    await fetch("http://localhost:8010/proxy/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": sessionStorage.getItem("usernametoken")
        },
        body: body64,
    }).then(function (response) {
        if (response.status == 200) {
            console.log("got user type");
            response.json().then(function (data) {
                console.log(data);
               //get user type from data and store in session storage);
               console.log(data.role);
                sessionStorage.setItem("role", data.role);
               
                //reditrect to the correct page
               window.location.href = "http://localhost:3031/home";
            });
        } else {
            console.log("failed to get user type");
            console.log(response);
        }
    }).catch(function (error) {
        console.log(error);
    });
};
