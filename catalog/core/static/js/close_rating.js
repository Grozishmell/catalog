document.addEventListener("DOMContentLoaded", function() {
    const statusSelect = document.getElementById('status');
    const userReview = "{{ user_review|yesno:'true,false' }}";  // Проверка на наличие отзыва

    // Если отзыв есть, блокируем выбор статуса и устанавливаем "просмотрено"
    if (userReview === 'true') {
        statusSelect.disabled = true;  // Блокируем поле выбора статуса
        statusSelect.value = 'watched';  // Устанавливаем статус на "просмотрено"
    }
});
