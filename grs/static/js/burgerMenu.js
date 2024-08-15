const burger = document.getElementById('burger');
const menu = document.getElementById('menu');
burger.addEventListener('click', () => {
    if (menu.style.display === 'block') {
        menu.style.display = 'none';
    }
    else{
        menu.style.display = 'block';
    }
});