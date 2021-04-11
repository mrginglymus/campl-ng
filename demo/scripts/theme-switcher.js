import Cookies from 'js-cookie';

function setTheme(theme) {
    Cookies.set('theme', theme);
    const clist = document.body.classList;
    if (!!clist) {
        clist.remove(clist.item(clist.length - 1));
    }
    clist.add(`theme-${theme}`);
}

const themes = [...document.querySelectorAll('a[data-toggle="theme"]')].map(a => a.dataset.colour);


setTheme(Cookies.get('theme') || 'turquoise');

document.querySelectorAll('a[data-toggle="theme"]').forEach($el => {
    $el.addEventListener('mouseup', e => {
        cancelDisco();
        setTheme($el.dataset.colour);
        e.preventDefault();
    })
})

let discoIndex = 0;
let disco = null;

function cancelDisco() {
    clearInterval(disco);
    disco = null;
}

const $discoButton = document.querySelector('a[href="#disco"]');
$discoButton.addEventListener('mouseup', e => {
    if (disco) {
        cancelDisco();
    } else {
        disco = setInterval(() => {
            discoIndex = (discoIndex + Math.floor(Math.random() * (themes.length - 1)) + 1) % themes.length
            setTheme(themes[discoIndex])
        }, 500)
    }
    e.preventDefault();
})
