// Login page: basic client-side checks before the form is submitted to Django.
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(".form-section form");
    if (!form) return;

    const username = document.getElementById("username");
    const password = document.getElementById("password");
    const submitBtn = form.querySelector(".submit-btn");

    form.addEventListener("submit", e => {
        username.value = username.value.trim();
        if (!username.value || !password.value) {
            e.preventDefault();
            alert("Please enter both your user name and password.");
            return;
        }
        submitBtn.disabled = true;
        submitBtn.textContent = "Signing in…";
    });
});
