var radioOwner = document.getElementById("ownerSelect");
var radioUser = document.getElementById("userSelect");
var phoneNumberText = document.getElementById("phoneNumber");

radioOwner.addEventListener("click", function () {
    phoneNumberText.style.display = "block";
});

radioUser.addEventListener("click", function () {
    phoneNumberText.style.display = "none";
});