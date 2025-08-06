

function login(){
    const account = document.getElementById("account").value;
    const password = document.getElementById("password").value;
    
    if (!account || !password) {
        alert("Vui lòng nhập đầy đủ tài khoản và mật khẩu.");
        return;
    }
    
    fetch("http://localhost:5000/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: account,
            password: password
        })
    })
    .then(response => {
        if (!response.ok) {
        // Có thể là 401 hoặc lỗi khác
        return response.text().then(text => {
            throw new Error(`Lỗi server: ${response.status} - ${text}`);
        });
        }
        return response.json();
    })
    .then(data => {
        if (data.status === "OKE") {
            alert("Đăng nhập thành công!");
            window.location.href = "../HTML/dashboard.html";
        } else {
            alert("Tài khoản hoặc mật khẩu không đúng. Vui lòng thử lại.");
        }
    })
    .catch(error => {
        console.error("Login error:", error);
        alert("Có lỗi xảy ra khi đăng nhập. Vui lòng thử lại.");
    });
}

// Make function available globally
window.login = login;


function togglePasswordVisibility() {
    const passwordInput = document.getElementById("password");
    const toggleButton = document.getElementById("toggle-password");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleButton.style.backgroundImage = "url('../HTML/assets/show-password.png')";
    } else {
        passwordInput.type = "password";
        toggleButton.style.backgroundImage = "url('../HTML/assets/hide-password.png')";
    }
}

// Make function available globally
window.togglePasswordVisibility = togglePasswordVisibility;

function togglePasswordVisibilityRegister() {
    const passwordInputRegister = document.getElementById("password-register");
    const toggleButtonRegister = document.getElementById("toggle-password-register");

    if (passwordInputRegister.type === "password") {
        passwordInputRegister.type = "text";
        toggleButtonRegister.style.backgroundImage = "url('../HTML/assets/show-password.png')";
    } else {
        passwordInputRegister.type = "password";
        toggleButtonRegister.style.backgroundImage = "url('../HTML/assets/hide-password.png')";
    }
}

// Make function available globally
window.togglePasswordVisibilityRegister = togglePasswordVisibilityRegister;

// Sign up
function sign_up() {
    document.getElementsByClassName("login-form")[0].style.display = "none";
    document.getElementsByClassName("sign-up-form")[0].style.display = "flex";
}

// Make function available globally
window.sign_up = sign_up;

function return_login() {
    document.getElementsByClassName("login-form")[0].style.display = "flex";
    document.getElementsByClassName("sign-up-form")[0].style.display = "none";
}

// Make function available globally
window.return_login = return_login;

function sign_up_submit() {
    const accountRegister = document.getElementById("account-register").value;
    const passwordRegister = document.getElementById("password-register").value;
    // const phoneNumber = document.getElementById("phone-number").value;
    const emailRegister = document.getElementById("email-register").value;
    
    if (!accountRegister || !passwordRegister || !emailRegister) {
        alert("Vui lòng nhập đầy đủ thông tin.");
        return;
    }
    
    fetch("http://localhost:5000/api/sign-up", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: accountRegister,
            email: emailRegister,
            password: passwordRegister
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.status === "OKE") {
            alert("Đăng ký thành công!");
            window.location.href = "../HTML/login.html";
        } else {
            if (data.message === "Username is empty") {
                alert("Tài khoản không được để trống.");
            }
            if (data.message === "Password is not valid") {
                alert("Mật khẩu không hợp lệ. Vui lòng nhập lại.(Ít nhất 1 số, 1 chữ, 1 ký tự đặc biệt)");
            }
            if (data.message === "Phone number is not valid") {
                alert("Số điện thoại không hợp lệ. Vui lòng nhập lại.");
            }
            if (data.message === "Username already exists") {
                alert("Tài khoản đã tồn tại. Vui lòng chọn tài khoản khác.");
            }
            if (data.message === "Email is not valid") {
                alert("Email không hợp lệ. Vui lòng nhập lại.");
            }
        }
    })
    .catch(error => {
        console.error("Sign up error:", error);
        alert("Có lỗi xảy ra khi đăng ký. Vui lòng thử lại.");
    });
}

// Make function available globally
window.sign_up_submit = sign_up_submit;