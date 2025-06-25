document.addEventListener("DOMContentLoaded", () => {
  const sr = ScrollReveal({
    distance: "20px",
    duration: 800,
    easing: "cubic-bezier(0.4, 0, 0.2, 1)",
    origin: "bottom",
    opacity: 0,
    reset: true, // para que la animación se repita
    mobile: true,
  });

  sr.reveal(".module-card", {
    interval: 150, // retardo escalonado de 150ms entre cards
  });
});
