document.addEventListener("DOMContentLoaded", function () {
  const userDropdown = document.getElementById("userDropdown");
  const userDropdownMenu = document.getElementById("userDropdownMenu");

  if (userDropdown && userDropdownMenu) {
    userDropdown.addEventListener("click", function (e) {
      e.preventDefault();
      if (userDropdownMenu) {
        userDropdownMenu.classList.toggle("hidden");
      }
    });

    document.addEventListener("click", function (e) {
      if (
        userDropdown &&
        userDropdownMenu &&
        !userDropdown.contains(e.target) &&
        !userDropdownMenu.contains(e.target)
      ) {
        userDropdownMenu.classList.add("hidden");
      }
    });
  } // Groups selector functionality
  const groupsSelector = document.querySelector("select");
  if (groupsSelector) {
    groupsSelector.addEventListener("change", function () {
      const selectedGroup = this.value;
      if (selectedGroup) {
        // Here you can add functionality to handle group selection
        console.log("Selected group:", selectedGroup);
        // You could make an AJAX request to change the user's active group
        // or redirect to a filtered view
      }
    });
  }

  // Add smooth entrance animations
  // Animate stats cards
  const statsCards = document.querySelectorAll(".grid > div");
  statsCards.forEach((card, index) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(20px)";
    setTimeout(() => {
      card.style.transition = "all 0.6s ease-out";
      card.style.opacity = "1";
      card.style.transform = "translateY(0)";
    }, index * 100);
  });

  // Add click ripple effect to buttons
  const buttons = document.querySelectorAll("button");
  buttons.forEach((button) => {
    button.addEventListener("click", function (e) {
      if (this.disabled) return;

      const ripple = document.createElement("span");
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;

      ripple.style.width = ripple.style.height = size + "px";
      ripple.style.left = x + "px";
      ripple.style.top = y + "px";
      ripple.classList.add("ripple");

      this.appendChild(ripple);

      setTimeout(() => {
        ripple.remove();
      }, 600);
    });
  });

  // Smooth scroll to modules on stats card click
  statsCards.forEach((card) => {
    card.addEventListener("click", function () {
      document
        .querySelector(".grid.grid-cols-1.md\\:grid-cols-2.lg\\:grid-cols-3")
        .scrollIntoView({
          behavior: "smooth",
        });
    });
  });
});

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

// Add intersection observer for animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.animation = "slideInRight 0.6s ease-out forwards";
    }
  });
}, observerOptions);

// Observe all module cards
document.querySelectorAll(".module-card").forEach((card) => {
  observer.observe(card);
});
document.getElementById("groupSelect").addEventListener("change", function () {
  const selectedGroupId = this.value;

  if (selectedGroupId) {
    // Redirigir con el parámetro gpid
    window.location.href = `${home}?gpid=${selectedGroupId}`;
  } else {
    // Si no hay selección, ir a la página sin parámetros
    window.location.href = home;
  }
});
