document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".star");
    const ratingInput = document.getElementById("rating-input");
    let selectedRating = 0; // Храним выбранный рейтинг

    stars.forEach(star => {
        star.addEventListener("mouseover", function () {
            resetStars();
            highlightStars(this.dataset.value);
        });

        star.addEventListener("click", function () {
            selectedRating = this.dataset.value; // Сохраняем выбор
            ratingInput.value = selectedRating;
            persistSelection();
        });

        star.addEventListener("mouseleave", function () {
            resetStars();
            persistSelection(); // Восстанавливаем только фиксированные звезды
        });
    });

    function resetStars() {
        stars.forEach(star => star.classList.remove("hovered", "selected"));
    }

    function highlightStars(value) {
        stars.forEach(star => {
            if (parseInt(star.dataset.value) <= parseInt(value)) {
                star.classList.add("hovered");
            }
        });
    }

    function persistSelection() {
        stars.forEach(star => {
            if (parseInt(star.dataset.value) <= parseInt(selectedRating)) {
                star.classList.add("selected");
            }
        });
    }
});