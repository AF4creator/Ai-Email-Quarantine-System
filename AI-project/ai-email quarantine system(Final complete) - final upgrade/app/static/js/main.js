console.log("Base JS loaded");

//THEME TOGGLE

const body = document.body;
const themeToggle = document.getElementById("themeToggle");

// Apply saved theme on load
const savedTheme = localStorage.getItem("theme");
if (savedTheme === "dark") {
  body.classList.add("dark");
  if (themeToggle) themeToggle.innerHTML = "☀️";
} else {
  if (themeToggle) themeToggle.innerHTML = "🌙";
}

// Toggle theme button event with smooth transition
if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    // Add transition class for smooth theme change
    body.style.transition = "background 0.3s ease, color 0.3s ease";
    
    body.classList.toggle("dark");

    const isDark = body.classList.contains("dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");

    themeToggle.innerHTML = isDark ? "☀️" : "🌙";
    
    // Remove transition after animation completes
    setTimeout(() => {
      body.style.transition = "";
    }, 300);
  });
}

//HAMBURGER MENU
const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("navLinks");

if (hamburger && navLinks) {
  hamburger.addEventListener("click", () => {
    const expanded = hamburger.getAttribute("aria-expanded") === "true" || false;

    navLinks.classList.toggle("active");
    hamburger.classList.toggle("open");

    hamburger.setAttribute("aria-expanded", !expanded);
  });

  // Close menu when clicking a nav link (improves mobile UX)
  navLinks.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("active");
      hamburger.classList.remove("open");
      hamburger.setAttribute("aria-expanded", "false");
    });
  });
}

//CLOSE MENU ON WINDOW RESIZE
window.addEventListener("resize", () => {
  if (window.innerWidth > 768 && navLinks && hamburger) {
    navLinks.classList.remove("active");
    hamburger.classList.remove("open");
    hamburger.setAttribute("aria-expanded", "false");
  }
});

// Form submission loading states
document.querySelectorAll("form").forEach(form => {
  form.addEventListener("submit", function(e) {
    const submitButton = this.querySelector('button[type="submit"]');
    if (submitButton && !submitButton.classList.contains("no-loading")) {
      submitButton.classList.add("loading");
      submitButton.disabled = true;
      submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    }
  });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href !== '#' && href !== '') {
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    }
  });
});

// Add fade-in animation to elements on scroll
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, observerOptions);

// Observe elements with fade-in class
document.querySelectorAll('.fade-in, .stat-card, .feature-card, .chart-box').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
  observer.observe(el);
});
