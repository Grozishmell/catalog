document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".rating-stars label");

    stars.forEach((star) => {
        star.addEventListener("click", function () {
            const radio = document.getElementById(this.getAttribute("for"));
            radio.checked = true;
            document.getElementById("rating-form").submit(); // Отправляем форму
        });
    });
});
