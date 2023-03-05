var radioOwner = document.getElementById("ownerSelect");
var radioUser = document.getElementById("userSelect");

var phoneNumberText = document.getElementById("phoneNumber"); //for display purposes
var registerButton = document.getElementById("buttonRegister");
var form = document.getElementById("registerForm");
//form elements
var username = document.getElementById("txtUsername");
var password = document.getElementById("txtPassword");
var nameTxt = document.getElementById("txtName");
var email = document.getElementById("txtEmail");
var phoneNumber = document.getElementById("txtNumber");


form.addEventListener("submit", function (ev) {
    ev.preventDefault();
});


radioOwner.addEventListener("click", function () {
    phoneNumberText.style.display = "block"; 
    //set the phone number to required
    phoneNumber.required = true; 
});

radioUser.addEventListener("click", function () {
    phoneNumberText.style.display = "none";
    //set the phone number to not required
    phoneNumber.required = false;
});

registerButton.addEventListener("click", async () => {
    //get the values from the form
    //if user is a store owner call a different endpioint
    if (radioOwner.checked == true) {
        let emailIsValid = validateEmail(email.value.toString());
        if (emailIsValid == false) {
            alert("Please enter a valid email address");
            return;
        }
        let phoneNumberIsValid = validatePhoneNumber(phoneNumber.value.toString());
        if (phoneNumberIsValid == false) {
            alert("Please enter a valid phone number");
            return;
        }
        registerOwner();
    }else if (radioUser.checked == true) {
        let emailIsValid = validateEmail(email.value.toString());
        if (emailIsValid == false) {
            alert("Please enter a valid email address");
            return;
        }
        let phoneNumberIsValid = validatePhoneNumber(phoneNumber.value.toString());
        if (phoneNumberIsValid == false) {
            alert("Please enter a valid phone number");
            return;
        }
        registerUser();
    }else {
        console.log("no radio button selected");
        alert("Please select a user type");
    }
});

//check if forme
//function to validate email address
function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

//function validate phone number
// ###-###-####
function validatePhoneNumber(phoneNumber) {
    var re = /^\d{3}-\d{3}-\d{4}$/;
    return re.test(phoneNumber);
}

//async function to register a owner
async function registerOwner() {

var user ={
    operation: "POST_Register_Proprietor",
    data: {
        name: nameTxt.value.toString(),
        username: username.value.toString(),
        password: password.value.toString(),
        email: email.value.toString(),
        phone: phoneNumber.value.toString()
    }
};


var userJSON = JSON.stringify(user);
var user64 = btoa(userJSON);
console.log("base 64 string "+ user64);

await fetch("http://localhost:8010/proxy/register", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: user64,
}).then(function (response) {
    if (response.status == 200) {
       console.log("owner registered");
         console.log(response);
         alert("Your account has been created");
    } else {
        console.log("login failed");
        console.log(response);
        //display error message in popup
        //take message from response and display it in a popup
        alert ("Registration failed: Username already exists");
    }
}).catch(function (error) {
    console.log("error: " + error);
});

}


//async function to register a user
async function registerUser() {

var user ={
    operation: "POST_Register_User",
    data: {
        name: nameTxt.value.toString(),
        username: username.value.toString(),
        password: password.value.toString(),
        email: email.value.toString()
    }
};

var userJSON = JSON.stringify(user);
var user64 = btoa(userJSON);
console.log("base 64 string "+ user64);

await fetch("http://localhost:8010/proxy/register", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: user64,
}).then(function (response) {
    if (response.status == 200) {
       console.log("user registered");
         console.log(response);
         alert("Your account has been created");
    } else {
        console.log("login failed");
        console.log(response);
        //display error message in popup
        //take message from response and display it in a popup
        alert ("Registration failed: Username already exists");
    }
}
).catch(function (error) {
    console.log("error: " + error);
});

}