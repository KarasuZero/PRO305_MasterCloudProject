var displayCartDiv = document.getElementById("displayCart");
var displayCartSection = document.getElementById("displayCartSection");

// go to cart page

window.onload = function () {
    displayCart();
};

function goToCartPage() {
    window.location.href = "http://localhost:3031/cart";
}


async function checkout(){
    console.log("checkout");
    let user = {
        "operation": "POST_Checkout",
        "data": {
            "username": sessionStorage.getItem("usernametoken"),
            "password": sessionStorage.getItem("password")
        }
    }
    let bodyJSON = JSON.stringify(user);
    let body64 = btoa(bodyJSON);
    console.log(body64);
    await fetch("http://localhost:8010/proxy/users", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "authorizationToken": sessionStorage.getItem("usernametoken")
        },
        body: body64
    }).then(function (response) {
        if (response.status == 200) {
            console.log("checked out");
            console.log(response);
            alert("Your order has been placed");
            EmptyCart();
            window.location.href = "http://localhost:3031/checkout";
        } else {
            console.log("failed to checkout");
            console.log(response);
        }
    }).catch(function (error) {
        console.log(error);
    });
}

async function EmptyCart() {
    console.log("empty cart");
    let user = {
        "operation": "POST_Clear_Cart",
        "data": {
            "username": sessionStorage.getItem("usernametoken"),
            "password": sessionStorage.getItem("password")
        }
    }
    let bodyJSON = JSON.stringify(user);
    let body64 = btoa(bodyJSON);
    console.log(body64);
    await fetch("http://localhost:8010/proxy/users", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "authorizationToken": sessionStorage.getItem("usernametoken")
        },
        body: body64
    }).then(function (response) {
        if (response.status == 200) {
            console.log("cart cleared");
            console.log(response);
            
        } else {
            console.log("failed to clear cart");
            console.log(response);
        }
    }).catch(function (error) {
        console.log(error);
    });
}

//function to display cart 
let cartList = []; //array to hold the list of menu items
async function displayCart() {
   let user ={
        "operation": "POST_Get_Cart",
        "data": {
            "username": sessionStorage.getItem("usernametoken"),
            "password": sessionStorage.getItem("password")
        }
    }
    let bodyJSON = JSON.stringify(user);
    let body64 = btoa(bodyJSON);
    console.log(body64);
    await fetch("http://localhost:8010/proxy/users", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "authorizationToken": sessionStorage.getItem("usernametoken")
        },
        body: body64
    }).then(function (response) {
        if (response.status == 200) {
            console.log("got cart");
            console.log(response);
            response.json().then(function (data) {
                console.log(data);
                cartList = data;
                console.log(cartList);
                //display cart 
                appendCart(cartList);

               
            });
        } else {
            console.log("failed to get cart");
            console.log(response);
        }
    }).catch(function (error) {
        console.log(error);
    }
    );
}

 function appendCart(cartlist) {
    console.log("appending cart");
    let total = 0.00;
    cartList.forEach(function (item) {
        var cartItem = document.createElement("div");
        cartItem.className = "cartItem";
        cartItem.id = item.item_id;
        cartItem.innerHTML = `
        <div class="card" style="width: 18rem;">
        <div class="card-body">
        <h3 class="card-title">${item.name}</h3>
        <h6 class="card-subtitle mb-2 text-muted">${item.price}</h6>
        <p class="card-text">${item.quantity}</p>
        <button style="background-color: rgb(249, 80, 80); outline-style: auto; outline-color: red; class="btn btn-primary btn-lg btn-block view-menu" id="${item.item_id}">Delete</button>
        </div>
        </div>
        `;
        displayCartSection.appendChild(cartItem);
        //add price string to total
        total += parseFloat(item.price);
        //add event listener to delete button
        const deleteButton = document.getElementById(item.item_id);
        deleteButton.addEventListener("click", function () {
            console.log("delete button clicked");
            deleteItem(item);
        });
    });
    //display total
    //display total to 2 decimal places
    total = total.toFixed(2);
    var totalDiv = document.createElement("div");
    totalDiv.className = "totalDiv";
    totalDiv.innerHTML = `
    <div class="card" style="width: 18rem;">
    <div class="card-body">
    <h3 class="card-title">Total</h3>
    <h6 class="card-subtitle mb-2 text-muted">$${total}</h6>
    </div>
    </div>
    `;
    displayCartSection.appendChild(totalDiv);

    //add a clear cart button 
    var clearCartButton = document.createElement("button");
    clearCartButton.className = "clearCartButton";
    clearCartButton.innerHTML = "Clear Cart";
    displayCartSection.appendChild(clearCartButton);
    clearCartButton.addEventListener("click", function () {
        EmptyCart();
    });
    
 }

async function deleteItem (item)  {
    //modify the cart
    let cartBody = {
        "operation": "PATCH_Modify_Cart",
        "data": {
            "username": sessionStorage.getItem("usernametoken"),
            "password": sessionStorage.getItem("password"),
            "menu_id": item.menu_id,
            "item_id": item.item_id,
            "quantity": "-1"
        } 
 }
    let bodyJSON = JSON.stringify(cartBody);
    let body64 = btoa(bodyJSON);
    console.log(body64);
    await fetch("http://localhost:8010/proxy/users", {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "authorizationToken": sessionStorage.getItem("usernametoken")
        },
        body: body64
    }).then(function (response) {
        if (response.status == 200) {
            //Save menu_id to cart_menu_id
            displayCart();
            console.log(response);
            alert("removed from cart");
        } else {
        }
    }).catch(function (error) {
        console.log(error);
    });
}
