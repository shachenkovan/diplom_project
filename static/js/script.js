// Получаем элементы для модальных окон
const modal = document.getElementById('myModal');
const openModal = document.getElementById('openModal');
const closeModal = document.getElementById('closeModal');

const contactModal = document.getElementById('contactModal');
const openContactModal = document.getElementById('openContactModal');
const closeContactModal = document.getElementById('closeContactModal');

// Открытие модального окна "О сайте"
openModal.onclick = function() {
    modal.style.display = 'block';
}

// Закрытие модального окна "О сайте"
closeModal.onclick = function() {
    modal.style.display = 'none';
}

// Открытие модального окна "Связаться"
openContactModal.onclick = function() {
    contactModal.style.display = 'block';
}

// Закрытие модального окна "Связаться"
closeContactModal.onclick = function() {
    contactModal.style.display = 'none';
}

// Закрытие модальных окон при клике вне окна
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    } else if (event.target == contactModal) {
        contactModal.style.display = 'none';
    }
}

