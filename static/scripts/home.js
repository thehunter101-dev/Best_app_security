document.addEventListener('DOMContentLoaded', () => {
    const sr = ScrollReveal({
        mobile: true,
    })

    // Revela todas las cards con animación escalonada
    sr.reveal('.module-card', {
        distance: '20px',
        duration: 800,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
        origin: 'bottom',
        opacity: 0,
        interval: 100,
        reset: true,
    })

    sr.reveal('.stats-card', {
        distance: '40px',
        duration: 800,
        origin: 'bottom',
        opacity: 0,
        reset: true,
    })

    sr.reveal('.section-card', {
        distance: '150%',
        duration: 800,
        origin: 'left',
        opacity: 0,
        interval: 100,
    })
})
