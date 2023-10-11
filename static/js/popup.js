// popup.js
const openButton = document.getElementById('open-popup');
const popup = document.getElementById('popup');
const closeButton = document.getElementById('close-popup');

openButton.addEventListener('click', () => {
    popup.style.display = 'block';
});

closeButton.addEventListener('click', () => {
    popup.style.display = 'none';
});
