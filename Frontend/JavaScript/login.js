function login(){
    window.location.href = "../HTML/dashboard.html";
}


function togglePasswordVisibility()
{
    const passwordInput = document.getElementById("password");
    const toggleButton = document.getElementsByClassName("toggle-password")[0];

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleButton.style.backgroundImage = "url('../HTML/assets/show-password.png')";
    } else {
        passwordInput.type = "password";
        toggleButton.style.backgroundImage = "url('../HTML/assets/hide-password.png')";
    }
}