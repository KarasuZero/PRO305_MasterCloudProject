var manageButton = document.getElementById("manageButton");
var resturauntList = document.getElementById("resturauntList");

//Only show manage button if user role is "Proprietor"
window.onload = function () {
    if (sessionStorage.getItem("role") == "PROPRIETOR") {
        manageButton.style.display = "block";
    }else
    {
        manageButton.style.display = "none";
    }

    //get the list of resturaunts from the database
    getResturaunts();
}

//function to get the list of resturaunts from the database

let restaurantList = []; //array to hold the list of resturaunts and their information
async function getResturaunts() {
    //Get the list of resturaunts from the database using operation GET_All_Store in the query string parameters
    //display the list of resturaunts on the page using innerHTML
    // each resturant has a div with class of "card-body p-4" and a button with class of "btn btn-primary btn-lg btn-block"
    //clicking the button will take the user to the resturaunt menu page
}


