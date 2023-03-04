var menuDisplay = document.getElementById("displayMenu");

//Call the API to get the menu on window load
window.onload = function () {
    getMenu();
};


//async function to get the menu

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
    await fetch(" http://localhost:8010/proxy/menu", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
        queryStringParameters: {
            "operation": "GET_Get_Menu",
            "menu_id": "570a76f6-b324-4b74-91d0-4bdfe952d119"
        },
    }).then(function (response) {
        if (response.status == 200) {
            console.log("got menu");
            response.json().then(function (data) {
                console.log(data);
                displayMenu(data);
            });
        } else {
            console.log("failed to get menu");
            console.log(response);
        }
    });

}

