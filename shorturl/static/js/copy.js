const copy_btn = document.querySelector('.short-url--btn');
const url = document.querySelector('.short-url--show');

if (copy_btn && url) {
    copy_btn.addEventListener('click', copy);

    function copy(event) {
        url.select();
        document.execCommand('copy');
    }
}