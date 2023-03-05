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
}


