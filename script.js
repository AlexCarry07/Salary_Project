function validateEmail() {
    let email = document.getElementById("email").value;

    if (!email.includes("@")) {
        alert("Please enter a valid email");
        return false;
    }
    return true;
}
