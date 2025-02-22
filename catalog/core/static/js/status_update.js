function updateStatus(selectElement) {
    // Получаем новый статус
    var status = selectElement.value;
    var itemId = selectElement.getAttribute('data-item-id');  // Получаем ID элемента из атрибута data-item-id

    // Отправляем данные на сервер через AJAX
    fetch("/item/" + itemId + "/update-status/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ status: status, item_id: itemId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Статус обновлен");
        } else {
            console.log("Произошла ошибка");
        }
    })
    .catch(error => console.log('Ошибка:', error));
}
