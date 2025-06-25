document.addEventListener('DOMContentLoaded', function () {
    const sr = ScrollReveal({
        reset: true,
    })
    const userDropdown = document.getElementById('userDropdown')
    const userDropdownMenu = document.getElementById('userDropdownMenu')

    if (userDropdown && userDropdownMenu) {
        userDropdown.addEventListener('click', function (e) {
            e.preventDefault()
            if (userDropdownMenu) {
                userDropdownMenu.classList.toggle('hidden')
                sr.reveal(userDropdownMenu, {
                    origin: 'top',
                    distance: '50px',
                    duration: 400,
                    opacity: 0,
                    easing: 'ease-out',
                })
            }
        })

        document.addEventListener('click', function (e) {
            if (
                userDropdown &&
                userDropdownMenu &&
                !userDropdown.contains(e.target) &&
                !userDropdownMenu.contains(e.target)
            ) {
                userDropdownMenu.classList.add('hidden')
                sr.reveal(userDropdownMenu, {
                    origin: 'top',
                    distance: '50px',
                    duration: 400,
                    opacity: 1,
                    easing: 'ease-in',
                })
            }
        })
    } // Groups selector functionality
    const groupsSelector = document.querySelector('select')
    if (groupsSelector) {
        groupsSelector.addEventListener('change', function () {
            const selectedGroup = this.value
            if (selectedGroup) {
                // Here you can add functionality to handle group selection
                console.log('Selected group:', selectedGroup)
                // You could make an AJAX request to change the user's active group
                // or redirect to a filtered view
            }
        })
    }

    // Add smooth entrance animations
    // Animate stats cards
    const statsCards = document.querySelectorAll('.grid > div')
    statsCards.forEach((card, index) => {
        card.style.opacity = '0'
        card.style.transform = 'translateY(20px)'
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease-out'
            card.style.opacity = '1'
            card.style.transform = 'translateY(0)'
        }, index * 100)
    })

    // Add click ripple effect to buttons

    // Smooth scroll to modules on stats card click
    statsCards.forEach((card) => {
        card.addEventListener('click', function () {
            document
                .querySelector('.grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-3')
                .scrollIntoView({
                    behavior: 'smooth',
                })
        })
    })
})

/*
document.getElementById('groupSelect').addEventListener('change', function() {
    const selectedGroupId = this.value;

    if (selectedGroupId) {
        // Redirigir con el parámetro gpid
        window.location.href = `${home}?gpid=${selectedGroupId}`;
    } else {
        // Si no hay selección, ir a la página sin parámetros
        window.location.href = home;
    }
});
*/

document.getElementById('groupSelect').addEventListener('change', function () {
    const selectedGroupId = this.value

    if (selectedGroupId) {
        // Redirigir con el parámetro gpid
        window.location.href = `${home}?gpid=${selectedGroupId}`
    } else {
        // Si no hay selección, ir a la página sin parámetros
        window.location.href = home
    }
})
