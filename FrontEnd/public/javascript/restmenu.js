var menuDisplay = document.getElementById("displayMenu");
var menuDsiplaySection = document.getElementById("displayMenuSection");
// go to cart page
function goToCartPage() {
    console.log("go to cart page");
    window.location.href = "http://localhost:3031/cart";
}
//Call the API to get the menu on window load
window.onload = function () {
    getMenu();
};

async function EmptyCart() {
let userbody = {
        "operation": "POST_Clear_Cart",
        "data": {
            "username": sessionStorage.getItem("username"),
            "password": sessionStorage.getItem("password")
        }

}
let bodyJSON = JSON.stringify(userbody);
let body64 = btoa(bodyJSON);
console.log(body64);
await fetch("http://localhost:8010/proxy/user", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "authorizationToken": sessionStorage.getItem("usernametoken")

}
}).then(function (response) {
    if (response.status == 200) {
        console.log("cart cleared");
        console.log(response);
        alert("Cart Cleared");
    } else {
        console.log("failed to clear cart");
        console.log(response);
    }
}).catch(function (error) {
    console.log(error);
});
}


async function addToCart(item) {
    //only add to cart if there isnt an item from another restaurant in the cart
var isSameStore = false;
    if (sessionStorage.getItem("menu_id") == sessionStorage.getItem("cart_menu_id")) {
        isSameStore = true;
    }
    else if (sessionStorage.getItem("cart_menu_id") == null) {
        isSameStore = true;
    }
    else {
        isSameStore = false;
    }
    if (isSameStore = false) {
        alert("You already have an item from another store in your cart.  We will empty your cart and add this item.");
        //empty cart
        EmptyCart();
    }
  
    let cartBody = {
        "operation": "PATCH_Modify_Cart",
        "data": {
            "username": sessionStorage.getItem("usernametoken"),
            "password": sessionStorage.getItem("password"),
            "menu_id": sessionStorage.getItem("menu_id"),
            "item_id": item.item_id,
            "quantity": "1"
        }
    }
    let bodyJSON = JSON.stringify(cartBody);
    let body64 = btoa(bodyJSON);
    console.log(body64);
    await fetch("http://localhost:8010/proxy/users", {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "authorizationToken": sessionStorage.getItem("usernametoken"),
        },
        body: body64
    }).then(function (response) {
        if (response.status == 200) {
            //Save menu_id to cart_menu_id
            sessionStorage.setItem("cart_menu_id", sessionStorage.getItem("menu_id"));
            console.log("added to cart");
            console.log(response);
            alert("Added to cart");
        } else {
        }
    }).catch(function (error) {
        console.log(error);
    });
}

//async function to get the menu
let menuList = []; //array to hold the list of menu items
async function getMenu() {
    let menuBody = { 
        "operation": "GET_Get_Menu",
        "data": {
            "menu_id": "570a76f6-b324-4b74-91d0-4bdfe952d119"
        }
    }

    //query string sends in the operation and menu id

    let bodyJSON = JSON.stringify(menuBody);
    let body64 = btoa(bodyJSON);

    console.log(body64);
    await fetch(`http://localhost:8010/proxy/menu?operation=GET_Get_Menu&menu_id=${sessionStorage.getItem("menu_id")}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    }).then(function (response) {
        if (response.status == 200) {
            console.log("got menu");
            response.json().then(function (data) {
                console.log(data);
               //put menu items into the menuList array, items array  is within the data  whithin item 
              
               
                menuList = data.items;
                console.log("menu: "+ menuList);
                //use innerHTML display each menu item with a add to cart button along with the name, description, and price
                //when the button is clicked, add the item to the cart it will call a function that will call and endpoint to add the item to the cart
                //this function needs menu_id and item_id and a quantity of 1
                //send the menu_id and item_id to the cart funtcion
               
                
                appendMenu(menuList);

            }); 
        } else {
            console.log("failed to get menu");
            console.log(response);
        }
    }).catch(function (error) {
        console.log(error);
    }
    );
}



function appendMenu(menuList) {
    console.log("Attempting to append menu");
    menuList.forEach(function (item) {
        console.log(item);
        const menuItem = document.createElement("div");
        menuItem.classList.add("card");
        menuItem.style.width = "18rem";
        menuItem.innerHTML += `
        <div class="card" style="width: 18rem;">
        <div class="card-body">

            <h5 class="card-title">${item.name}</h5>
            <h6 class="card-subtitle mb-2 text-muted">${item.price}</h6>
            <p class="card-text">${item.description}</p>
            <button style="background-color: rgb(249, 80, 80); outline-style: auto; outline-color: red; class="btn btn-primary btn-lg btn-block view-menu" id="${item.item_id}">Add to Cart</a>
        </div>
    </div>
            `;
       

            menuDsiplaySection.appendChild(menuItem);
            //create event listener that sends the item to the add to cart function
           const addToCartBtn = document.getElementById(item.item_id);
            addToCartBtn.addEventListener("click", function () {
                console.log("add to cart button clicked");
                addToCart(item);
            });
    });
}

