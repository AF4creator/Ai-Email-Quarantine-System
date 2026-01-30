function scanDemo() {
  const url = document.getElementById('demoUrl').value;
  const result = document.getElementById('demoResult');
  if (!url) return;
  // Simulate scan
  setTimeout(() => {
    result.innerHTML = '<i class="fas fa-shield-check"></i> <strong>Safe</strong> (Score: 0.12)';
    result.className = 'result safe';
  }, 1000);
}

// Enhanced FAQ accordion with smooth animations
document.querySelectorAll(".faq-question").forEach(button => {
  button.addEventListener("click", () => {
    const item = button.parentElement;
    const isActive = item.classList.contains("active");
    
    // Close all other FAQ items
    document.querySelectorAll(".faq-item").forEach(otherItem => {
      if (otherItem !== item) {
        otherItem.classList.remove("active");
      }
    });
    
    // Toggle current item
    item.classList.toggle("active", !isActive);
    
    // Smooth scroll to active FAQ item
    if (!isActive) {
      setTimeout(() => {
        item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 100);
    }
  });
});

// Add animation to stats on scroll
const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const statItem = entry.target;
      const number = statItem.querySelector('h3');
      if (number && !statItem.classList.contains('animated')) {
        statItem.classList.add('animated');
        animateNumber(number);
      }
    }
  });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-item').forEach(item => {
  statsObserver.observe(item);
});

function animateNumber(element) {
  const target = parseInt(element.textContent.replace(/[^0-9]/g, ''));
  const duration = 2000;
  const increment = target / (duration / 16);
  let current = 0;
  
  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      element.textContent = element.textContent.replace(/[0-9]+/, target);
      clearInterval(timer);
    } else {
      const displayValue = Math.floor(current);
      element.textContent = element.textContent.replace(/[0-9]+/, displayValue);
    }
  }, 16);
}

