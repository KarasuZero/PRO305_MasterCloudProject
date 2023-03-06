var displayCart = getElementById("displayCart");

window.onload = function () {
    displayCart();
};
//function to display cart 
let cartList = []; //array to hold the list of menu items
async function displayCart() {
    user ={
        "operation": "POST_Get_Cart",
        "data": {
            "username": sessionStorage.getItem("username"),
            "password": sessionStorage.getItem("password"),
        }
    }
    let bodyJSON = JSON.stringify(user);
    let body64 = btoa(bodyJSON);
    console.log(body64);
    await fetch("http://localhost:8010/proxy/user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "authToken": sessionStorage.getItem("usernametoken")
        },
        body: body64
    }).then(function (response) {
        if (response.status == 200) {
            console.log("got cart");
            console.log(response);
            response.json().then(function (data) {
                console.log(data);
                cartList = data.item;
                console.log(cartList);
                //display cart 
                for (let i = 0; i < cartList.length; i++) {
                }

               
            });
        } else {
            console.log("failed to get user type");
            console.log(response);
        }
    }).catch(function (error) {
        console.log(error);
    }
    );
}
