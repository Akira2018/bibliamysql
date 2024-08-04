document.addEventListener('DOMContentLoaded', function() {
    var toggleNavButton = document.querySelector('.nav-toggler');
    var sideNav = document.querySelector('#nav-sidebar');

    if (toggleNavButton && sideNav) {
        sideNav.classList.add('collapsed');

        toggleNavButton.addEventListener('click', function() {
            sideNav.classList.toggle('collapsed');
        });

        // Recolher o menu lateral quando uma opção do menu superior for clicada
        var topMenuLinks = document.querySelectorAll('.custom-admin-menu a');
        topMenuLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                sideNav.classList.add('collapsed');
            });
        });
    }
});

