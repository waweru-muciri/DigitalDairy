document.addEventListener('DOMContentLoaded', function () {
    var x = document.querySelectorAll("a[href^='#']");
    x.forEach(element => {
        if (element.hasAttribute('data-scrollto')) {
            element.addEventListener('click', function (event) {
                var to_element = document.getElementById(element.getAttribute('data-scrollto'));
                to_element.scrollIntoView({ behavior: 'smooth' });
            })
        }
    });
    document.addEventListener("scroll", function (event) {
        if (document.body.scrollTop < 100 || document.documentElement.scrollTop < 100) {
            document.getElementById('scroll-top').classList.add('d-none')
        } else {
            document.getElementById('scroll-top').classList.add('d-block')
        }
    })
})