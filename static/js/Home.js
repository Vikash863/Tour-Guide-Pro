// === Authentication Handler ===
function initializeAuth() {
  const loginIcon = document.getElementById('loginIcon');
  const userDropdown = document.getElementById('userDropdown');
  const userNameDisplay = document.getElementById('userNameDisplay');

  if (auth.isLoggedIn()) {
    const user = auth.getUser();
    if (user) {
      userNameDisplay.textContent = `Hello, ${user.name}!`;
      loginIcon.style.cursor = 'pointer';
      loginIcon.addEventListener('click', () => {
        userDropdown.classList.toggle('active');
      });

      // Close dropdown when clicking outside
      document.addEventListener('click', (e) => {
        if (!e.target.closest('.auth-icon')) {
          userDropdown.classList.remove('active');
        }
      });
    }
  } else {
    loginIcon.addEventListener('click', () => {
      window.location.href = '/login/';
    });
  }
}

// === Smooth scroll for navigation links ===
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href.startsWith('#')) {
      e.preventDefault();
      const targetId = href.substring(1);
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        targetSection.scrollIntoView({ behavior: 'smooth' });
      }
    }
  });
});

// === Mobile menu toggle (optional) ===
const navToggle = document.querySelector('.login-btn');
if (navToggle) {
  navToggle.addEventListener('click', () => {
    document.querySelector('.nav-links').classList.toggle('active');
  });
}

// === Auto-slideshow for destination cards ===
document.querySelectorAll(".card").forEach((card) => {
  const img = card.querySelector("img");
  const imagesAttr = card.getAttribute("data-images");

  if (!img || !imagesAttr) return;

  const images = JSON.parse(imagesAttr);
  let index = 0;

  setInterval(() => {
    index = (index + 1) % images.length;
    img.src = images[index];
  }, 1000); // Change image every 3 seconds
});



  const heroSection = document.querySelector('.hero-section');
  const images = [
    '/static/images/kerala1.jpg',
    '/static/images/ladakh8.jpg',
    '/static/images/kerala3.jpg',
    '/static/images/ladakh4.jpg',
    '/static/images/kerala5.jpg',
    '/static/images/goa1.jpg',
    '/static/images/goa2.jpg',
    '/static/images/goa3.jpg',
    '/static/images/varanasi4.jpg',
    '/static/images/jaipur5.jpg',
    '/static/images/goa10.jpg',
    '/static/images/jaipur2.jpg',
    '/static/images/varanasi3.jpg',
    '/static/images/varanasi2.jpg',
    '/static/images/ladakh1.jpg'
  ];

  let current = 0;

  function changeBackground() {
    heroSection.style.background = `url('${images[current]}') no-repeat center center / cover`;
    heroSection.style.backgroundAttachment = 'fixed';
    current = (current + 1) % images.length;
  }

  // Initial load
  changeBackground();

  // Change every 5 seconds
  setInterval(changeBackground, 5000);


  // how it works section animation
const stepCards = document.querySelectorAll('.step-card');

stepCards.forEach((card, index) => {
  card.style.opacity = 0;
  card.style.transform = 'translateY(30px)';
  setTimeout(() => {
    card.style.transition = 'all 0.6s ease-out';
    card.style.opacity = 1;
    card.style.transform = 'translateY(0)';
  }, 300 * index);
});


// === Testimonials Carousel ===

const testimonialCards = document.querySelectorAll('.testimonial-card');
let currentTestimonial = 0;

function showTestimonial(index) {
  testimonialCards.forEach((card, i) => {
    card.classList.toggle('active', i === index);
  });
}

document.getElementById('nextTestimonial').addEventListener('click', () => {
  currentTestimonial = (currentTestimonial + 1) % testimonialCards.length;
  showTestimonial(currentTestimonial);
});

document.getElementById('prevTestimonial').addEventListener('click', () => {
  currentTestimonial = (currentTestimonial - 1 + testimonialCards.length) % testimonialCards.length;
  showTestimonial(currentTestimonial);
});


//for header section

// Smooth scroll for internal links
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href.startsWith('#')) {
      e.preventDefault();
      const targetId = href.substring(1);
      const targetSection = document.getElementById(targetId);
      if (targetSection) {
        targetSection.scrollIntoView({ behavior: 'smooth' });
      }
    }
  });
});

// Redirect on login icon click
document.getElementById('loginIcon').addEventListener('click', () => {
  window.location.href = '/login/';
});

// Initialize auth on page load
document.addEventListener('DOMContentLoaded', initializeAuth);