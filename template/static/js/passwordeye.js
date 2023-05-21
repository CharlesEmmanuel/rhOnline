
var togglePassword = document.getElementById("togglePassword");

togglePassword.addEventListener("click", function() {
var password = document.getElementById("password");
if (password.type === "password") {
password.type = "text";
togglePassword.innerHTML = '<i class="fa fa-eye"></i>';
} else {
password.type = "password";
togglePassword.innerHTML = '<i class="fa fa-eye-slash"></i>';
}
});