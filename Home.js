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
    'images/kerala1.jpg',
    'images/ladakh8.jpg',
    'images/kerala3.jpg',
    'images/ladakh4.jpg',
    'images/kerala5.jpg',
    'images/goa1.jpg',
    'images/goa2.jpg',
    'images/goa3.jpg',
    'images/varanasi4.jpg',
    'images/jaipur5.jpg',
    'images/goa10.jpg',
    'images/jaipur2.jpg',
    'images/varanasi3.jpg',
    'images/varanasi2.jpg',
    'images/ladakh1.jpg'
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
  window.location.href = 'login.html';
});


// Redirect on login icon click
document.getElementById('loginIcon').addEventListener('click', () => {
  window.location.href = 'login.html'; // or 'signup.html' if you prefer
});