var manageButton = document.getElementById("manageButton");
var resturauntListDoc = document.getElementById("restaurantList");
var resturantSection = document.getElementById("restaurants");

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
    await fetch("http://localhost:8010/proxy/users?operation=GET_All_Store", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            //"authorizationToken ": sessionStorage.getItem("usernametoken")
        },
    }).then(function (response) {
        if (response.status == 200) {
            console.log("got resturaunts");
            response.json().then(function (data) {
                console.log(data);
              
                
                restaurantList = data;
                console.log(restaurantList);
                
                
                //Resturants have store_name, desc, loc, city, st, zip, phone, email, hours, website, menu_list
                //loc , city, st, zip, can be combined into one string
                //menu list contains an id that will be used to get the menu items when button is clicked
                //store menu_id in session storage to use in the menu page
                appendCatalog(restaurantList);
            }). catch(function (error) {
                console.log(error);
            });
        } else {
            console.log("error getting resturaunts");
            console.log(response);
        }
    }).catch(function (error) {
        console.log(error);
    });
    }

//function to append the resturaunt list to the page
function appendCatalog(restaurantList) {
    console.log("Attempting to append catalog");
    
    restaurantList.forEach((restaurant) => {
        //create random number from 3-1 to use in the image url
        const randomNum = Math.floor(Math.random() * (3 - 1 + 1) + 1);
        const restaurantListDoc = document.createElement("div");
        restaurantListDoc.classList.add("card-body", "p-4", "catalong-resturaunt");
        restaurantListDoc.innerHTML = `
        <div class="row" id="cssRest">
            <div class="col-md-4 ">
                <img src="https://loremflickr.com/320/240/food?random=${randomNum}" alt="resturaunt image" class="img-fluid">
            </div>
            <div class="col-md-8" id="cssDes">
                <h3>${restaurant.store_name}</h3>
                <p>${restaurant.description}</p>
                <p>${restaurant.loc}, ${restaurant.city}, ${restaurant.st}, ${restaurant.zipcode}</p>
                <p>${restaurant.phone}</p>
                <p>${restaurant.email}</p>
                <p>${restaurant.hours}</p>
                <p>${restaurant.website}</p>
                <button style="background-color: rgb(249, 80, 80); outline-style: auto; outline-color: red; class="btn btn-primary btn-lg btn-block view-menu"  id="${restaurant.store_name}">View Menu</button>
            </div>
        </div>
        `;
        resturauntListDoc.appendChild(restaurantListDoc);
        resturantSection.appendChild(resturauntListDoc);
        //create event listener for each button
        const viewMenuButton = document.getElementById(restaurant.store_name);
        viewMenuButton.addEventListener("click", function () {
            console.log("View Menu Button Clicked");
            sessionStorage.setItem("menu_id", restaurant.menu_list[0]);
            window.location.href = "http://localhost:3031/home/resturantMenu";
        });
    });


    }





