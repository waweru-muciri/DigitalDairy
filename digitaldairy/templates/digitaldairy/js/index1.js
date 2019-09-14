document.addEventListener('DOMContentLoaded', function () {
    var contactForm = document.forms['contactForm'];
    if (typeof contactForm !== 'undefined') {
        contactForm.addEventListener('submit', function (evt) {
            var formData = new FormData(contactForm);
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {
                    var response = JSON.parse(this.responseText)
                    var success_messages_div = document.getElementById('text-success');
                    success_messages_div.textContent = response.messages;
                    success_messages_div.classList.add('active');
                    //request focus to the element 
                    success_messages_div.focus();
                    contactForm.elements['first_name'].value = '';
                    contactForm.elements['last_name'].value = '';
                    contactForm.elements['email'].value = '';
                    contactForm.elements['phone_number'].value = '';
                    contactForm.elements['message'].value = '';
                }
            };
            xhttp.open('POST', contactForm.action, true);
            xhttp.send(formData);
            evt.preventDefault();
        });
    };
    var x = document.querySelectorAll("a[href^='#']");
    x.forEach(element => {
        if (element.hasAttribute('data-scrollto')) {
            element.addEventListener('click', function (event) {
                var to_element = document.getElementById(element.getAttribute('data-scrollto'));
                if (to_element == undefined) {
                    return;
                }
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