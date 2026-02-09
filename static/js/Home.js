// === User Dropdown Handler ===
function initializeAuth() {
  const loginIcon = document.getElementById('loginIcon');
  const userDropdown = document.getElementById('userDropdown');
  const userNameDisplay = document.getElementById('userNameDisplay');

  if (auth.isLoggedIn()) {
    const user = auth.getUser();
    if (user) {
      const displayName = user.first_name || user.name || user.username || 'User';
      
      // Update user name display
      if (userNameDisplay) {
        userNameDisplay.textContent = displayName;
      }

      // Toggle dropdown on click
      if (loginIcon && userDropdown) {
        loginIcon.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          userDropdown.classList.toggle('show');
        });
      }

      // Close dropdown when clicking outside
      document.addEventListener('click', (e) => {
        if (userDropdown && !e.target.closest('.auth-icon')) {
          userDropdown.classList.remove('show');
        }
      });
    }
  } else {
    // Show login icon for non-logged in users - click goes to login page
    if (loginIcon) {
      loginIcon.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = '/login/';
      });
    }
  }
}

// === Mobile Menu Toggle ===
function toggleMobileMenu() {
  const navLinks = document.getElementById('navLinks');
  if (navLinks) {
    navLinks.classList.toggle('active');
  }
}

// === User Dropdown Toggle ===
function toggleUserDropdown() {
  const userDropdown = document.getElementById('userDropdown');
  if (userDropdown) {
    userDropdown.classList.toggle('active');
  }
}

// === Logout Handler ===
// This is used by auth.logout() from the HTML
const auth = {
    isLoggedIn: () => !!localStorage.getItem('authToken'),
    
    getUser: () => {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    },
    
    logout: () => {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        sessionStorage.clear();
        // Redirect to home
        window.location.href = '/';
    }
};

function handleLogout() {
    auth.logout();
}

// === Smooth scroll for navigation links ===
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href && href.startsWith('#')) {
      e.preventDefault();
      const targetSection = document.getElementById(href.substring(1));
      if (targetSection) {
        targetSection.scrollIntoView({ behavior: 'smooth' });
      }
    }
  });
});

// === Auto-slideshow for hero section ===
const heroSection = document.querySelector('.hero-section');
const heroImages = [
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

let currentHero = 0;

function changeHeroBackground() {
  if (heroSection) {
    heroSection.style.background = `url('${heroImages[currentHero]}') no-repeat center center / cover`;
    heroSection.style.backgroundAttachment = 'fixed';
    currentHero = (currentHero + 1) % heroImages.length;
  }
}

// Initial hero background
changeHeroBackground();
// Change every 5 seconds
setInterval(changeHeroBackground, 5000);

// === Step cards animation ===
document.querySelectorAll('.step-card').forEach((card, index) => {
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

const nextBtn = document.getElementById('nextTestimonial');
const prevBtn = document.getElementById('prevTestimonial');

if (nextBtn) nextBtn.addEventListener('click', () => {
  currentTestimonial = (currentTestimonial + 1) % testimonialCards.length;
  showTestimonial(currentTestimonial);
});

if (prevBtn) prevBtn.addEventListener('click', () => {
  currentTestimonial = (currentTestimonial - 1 + testimonialCards.length) % testimonialCards.length;
  showTestimonial(currentTestimonial);
});

// === Chatbot (with null checks) ===
const chatbotToggle = document.getElementById('chatbot-toggle');
const chatbotPanel = document.getElementById('chatbot-panel');
const messagesDiv = document.getElementById('chatbot-messages');
const userInput = document.getElementById('chatbot-user-input');

// Toggle chatbot panel
if (chatbotToggle && chatbotPanel) {
  chatbotToggle.addEventListener('click', () => {
    chatbotPanel.style.display = chatbotPanel.style.display === 'flex' ? 'none' : 'flex';
  });
}

// Add message to chat
function addChatMessage(text, sender) {
  if (!messagesDiv) return;
  const div = document.createElement('div');
  div.classList.add('chat-message', sender);
  div.textContent = text;
  messagesDiv.appendChild(div);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Send message
async function sendChatbotMessage() {
  if (!userInput || !messagesDiv) return;
  const text = userInput.value.trim();
  if (!text) return;
  addChatMessage(text, 'user-message');
  userInput.value = '';
  addChatMessage('Thanks for your message! Our team will respond shortly.', 'bot-message');
}

// === Destination cards slideshow ===
document.querySelectorAll(".card[data-images]").forEach(card => {
  const img = card.querySelector("img");
  const images = JSON.parse(card.getAttribute("data-images"));
  let index = 0;

  if (!img || !images) return;

  setInterval(() => {
    index = (index + 1) % images.length;
    img.src = images[index];
  }, 3000);
});

// === Initialize on DOM load ===
document.addEventListener('DOMContentLoaded', initializeAuth);

// === Close mobile menu when clicking outside ===
document.addEventListener('click', (e) => {
  const navLinks = document.getElementById('navLinks');
  const mobileBtn = document.querySelector('.mobile-menu-btn');
  
  if (navLinks && navLinks.classList.contains('active')) {
    if (!e.target.closest('.nav-links') && !e.target.closest('.mobile-menu-btn')) {
      navLinks.classList.remove('active');
    }
  }
});

// === Close user dropdown when pressing Escape ===
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const userDropdown = document.getElementById('userDropdown');
    if (userDropdown && userDropdown.classList.contains('active')) {
      userDropdown.classList.remove('active');
    }
  }
});
