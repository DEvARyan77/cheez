function toggleMenu() {
    const leftMenu = document.getElementById('leftMenu');
    const rightPanel = document.getElementById('right-panel');
    if (leftMenu.style.width === '5%' || leftMenu.style.width === '') {
        leftMenu.style.width = '20%';
        rightPanel.style.width = '20%';
    } else {
        leftMenu.style.width = '5%';
        rightPanel.style.width = '55%';
    }
}

function adjustPageWidth() {
    const width = window.innerWidth;
    const body = document.body;

    if (width >= 992 && width <= 1600) {
        body.style.transform = 'scale(0.9)';
    } else if (width >= 700 && width <= 767) {
        body.style.transform = 'scale(0.8)';
    } else if (width >= 600 && width <= 700) {
        body.style.transform = 'scale(0.75)';
    } else if (width <= 600) {
        body.style.transform = 'scale(0.5)';
    } else {
        body.style.transform = 'scale(1)';
    }
}

window.addEventListener('resize', adjustPageWidth);
window.addEventListener('load', adjustPageWidth);