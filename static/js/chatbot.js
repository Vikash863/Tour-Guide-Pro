// TourGuidePro Chatbot
var tourGuideChatbot;

document.addEventListener('DOMContentLoaded', function() {
    tourGuideChatbot = {
        isOpen: false,
        messages: [],
        init: function() {
            this.createWidget();
            this.bindEvents();
            this.loadWelcomeMessage();
        },
        createWidget: function() {
            var html = '<div class="chatbot-widget"><div class="chatbot-container" id="chatbotContainer"><div class="chatbot-header"><div class="chatbot-avatar"><i class="bi bi-compass"></i></div><div class="chatbot-title"><h3>TourGuide Pro</h3><p>Your Travel Assistant</p></div><button class="chatbot-close" id="chatbotClose"><i class="bi bi-x-lg"></i></button></div><div class="chatbot-messages" id="chatbotMessages"></div><div class="chatbot-input-area"><input type="text" class="chatbot-input" id="chatbotInput" placeholder="Ask me about your trip..."><button class="chatbot-send" id="chatbotSend"><i class="bi bi-send"></i></button></div></div><button class="chatbot-toggle" id="chatbotToggle"><i class="bi bi-chat-dots"></i></button></div>';
            document.body.insertAdjacentHTML('beforeend', html);
        },
        bindEvents: function() {
            var self = this;
            document.getElementById('chatbotToggle').onclick = function() { self.toggleChat(); };
            document.getElementById('chatbotClose').onclick = function() { self.closeChat(); };
            document.getElementById('chatbotSend').onclick = function() { self.handleSend(); };
            document.getElementById('chatbotInput').onkeypress = function(e) { if (e.key === 'Enter') self.handleSend(); };
        },
        toggleChat: function() {
            this.isOpen = !this.isOpen;
            var container = document.getElementById('chatbotContainer');
            if (this.isOpen) container.classList.add('active');
            else container.classList.remove('active');
            if (this.isOpen) setTimeout(function() { document.getElementById('chatbotInput').focus(); }, 300);
        },
        closeChat: function() {
            this.isOpen = false;
            document.getElementById('chatbotContainer').classList.remove('active');
        },
        loadWelcomeMessage: function() {
            var self = this;
            setTimeout(function() {
                self.addBotMessage("Hi! I'm your TourGuide Pro assistant. I can help you with:\n\n* Hotels - Find best hotels with prices\n* Destinations - Explore top tourist places\n* Trip Planning - Create perfect itineraries\n* Cabs - Book taxis and transport\n* Weather - Best time to visit\n* Budget - Estimate trip costs\n* Food - Famous local cuisine\n\nWhat would you like to know?");
                self.addQuickReplies(["Hotels in Delhi", "Popular destinations", "Plan my trip", "Book a cab"]);
            }, 500);
        },
        addMessage: function(text, type) {
            var container = document.getElementById('chatbotMessages');
            var div = document.createElement('div');
            div.className = 'message ' + type;
            var time = new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
            div.innerHTML = text.replace(/\n/g, '<br>') + '<div class="message-time">' + time + '</div>';
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        },
        addBotMessage: function(text) { this.addMessage(text, 'bot'); },
        addUserMessage: function(text) { this.addMessage(text, 'user'); },
        addQuickReplies: function(replies) {
            var container = document.getElementById('chatbotMessages');
            var div = document.createElement('div');
            div.className = 'quick-replies';
            var self = this;
            replies.forEach(function(reply) {
                var btn = document.createElement('button');
                btn.className = 'quick-reply';
                btn.textContent = reply;
                btn.onclick = function() { self.handleSend(reply); };
                div.appendChild(btn);
            });
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        },
        showTypingIndicator: function() {
            var container = document.getElementById('chatbotMessages');
            var div = document.createElement('div');
            div.className = 'typing-indicator';
            div.id = 'typingIndicator';
            div.innerHTML = '<span></span><span></span><span></span>';
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        },
        hideTypingIndicator: function() {
            var el = document.getElementById('typingIndicator');
            if (el) el.remove();
        },
        handleSend: function(text) {
            var input = document.getElementById('chatbotInput');
            var message = text || input.value.trim();
            if (!message) return;
            input.value = '';
            var qr = document.querySelector('.quick-replies');
            if (qr) qr.remove();
            this.addUserMessage(message);
            this.showTypingIndicator();
            var self = this;
            setTimeout(function() {
                self.hideTypingIndicator();
                var response = self.getBotResponse(message);
                self.addBotMessage(response.text);
                if (response.quickReplies) self.addQuickReplies(response.quickReplies);
            }, 800);
        },
        getBotResponse: function(msg) {
            var message = msg.toLowerCase();
            
            if (message.indexOf('hotel') !== -1 || message.indexOf('stay') !== -1) {
                return {text: "HOTEL BOOKING GUIDE\n\nPopular Hotel Chains:\n- Taj Hotels: Luxury (8000-50000/night)\n- OYO: Budget (500-2000/night)\n- Marriott: Premium (5000-25000/night)\n- Hilton: Luxury (10000-40000/night)\n\nAmenities:\n- Free WiFi, Breakfast, Pool\n- Gym, Parking, Room service\n\nTips:\n- Book 2-4 weeks in advance\n- Check cancellation policy", quickReplies: ['Hotels in Delhi', 'Hotels in Mumbai', 'Hotels in Goa', 'Hotels in Jaipur']};
            }
            
            if (message.indexOf('weather') !== -1 || message.indexOf('climate') !== -1) {
                return {text: "BEST TIME TO VISIT\n\nDelhi: Oct-Mar (15-30C)\nGoa: Nov-Feb (22-32C)\nJaipur: Oct-Mar (10-30C)\nKerala: Sep-Mar (24-33C)\nLadakh: May-Sep (10-25C)\nMumbai: Oct-Feb (18-32C)\nAgra: Oct-Mar (10-30C)", quickReplies: ['Delhi weather', 'Goa weather', 'Jaipur weather', 'Ladakh weather']};
            }
            
            if (message.indexOf('destination') !== -1 || message.indexOf('place') !== -1 || message.indexOf('visit') !== -1) {
                return {text: "POPULAR DESTINATIONS\n\nHistorical:\n- Agra: Taj Mahal (2-3 days)\n- Jaipur: Amber Fort (2-3 days)\n- Varanasi: Ghats (2 days)\n\nBeaches:\n- Goa: Baga, Palolem (4-7 days)\n- Kerala: Backwaters (5-7 days)\n\nMountains:\n- Ladakh: Pangong Lake (7-10 days)\n- Manali: Rohtang (3-5 days)", quickReplies: ['Taj Mahal info', 'Goa beaches', 'Ladakh adventure', 'Kerala backwaters']};
            }
            
            if (message.indexOf('itinerary') !== -1 || message.indexOf('plan') !== -1 || message.indexOf('trip') !== -1) {
                return {text: "TRIP PLANNING GUIDE\n\nWeekend (2-3 days):\nDay 1: Arrive, check-in, sightseeing\nDay 2: Full day tour\nDay 3: Checkout, return\n\nWeek-long (7 days):\nDays 1-2: Main destination\nDays 3-4: Nearby attractions\nDay 5: Adventure activities\nDay 6: Shopping\nDay 7: Relax and depart\n\nTips:\n- Book accommodations early\n- Plan 1-2 activities per day", quickReplies: ['2-3 days plan', 'Week-long trip', 'Budget trip', 'Luxury vacation']};
            }
            
            if (message.indexOf('cab') !== -1 || message.indexOf('taxi') !== -1 || message.indexOf('transport') !== -1) {
                return {text: "CAB AND TRANSPORT\n\nCab Services:\n- Uber/Ola: App-based (8-20/km)\n- Local Taxis: City travel\n- Outstation: Long distance\n- Self-Drive: Rent a car\n\nEstimated Costs:\n- City tour (8 hrs): 1500-3000\n- Airport pickup: 500-2000\n- Outstation: 10-25/km\n\nPopular Routes:\nDelhi-Agra: 3000-5000\nMumbai-Pune: 2000-3500", quickReplies: ['Book airport cab', 'City tour cab', 'Outstation trip']};
            }
            
            if (message.indexOf('cost') !== -1 || message.indexOf('price') !== -1 || message.indexOf('budget') !== -1) {
                return {text: "BUDGET PLANNING\n\nBudget Trip (5000-10000):\n- Hostels: 200-500/night\n- Local food: 100-200/day\n\nMid-Range (10000-25000):\n- 3-star hotel: 1500-3000/night\n- Restaurant meals: 300-500/day\n\nLuxury (50000+):\n- 5-star hotel: 10000-50000/night\n- Fine dining: 1000-3000/day", quickReplies: ['Budget trip', 'Mid-range trip', 'Luxury vacation']};
            }
            
            if (message.indexOf('food') !== -1 || message.indexOf('cuisine') !== -1) {
                return {text: "LOCAL CUISINE\n\nNorth India:\n- Butter Chicken, Naan, Biryani\n- Chole Bhature, Lassi\n\nSouth India:\n- Dosa, Idli, Sambar\n- Hyderabadi Biryani\n\nWest India:\n- Goan Fish Curry\n- Pav Bhaji, Vada Pav\n\nStreet Food Hubs:\n- Delhi: Chandni Chowk\n- Mumbai: Juhu Beach", quickReplies: ['North Indian food', 'South Indian food', 'Street food Delhi', 'Goa cuisine']};
            }
            
            // City-specific
            if (message.indexOf('delhi') !== -1) {
                return {text: "DELHI - The Capital City\n\nTop Attractions:\n- India Gate, Qutub Minar\n- Red Fort, Humayun's Tomb\n- Chandni Chowk (shopping)\n- Lotus Temple, Akshardham\n\nBest Time: Oct-Mar (15-30C)\nStay: 500-50000/night", quickReplies: ['Hotels in Delhi', 'Things to do', 'Delhi weather']};
            }
            
            if (message.indexOf('mumbai') !== -1) {
                return {text: "MUMBAI - City of Dreams\n\nTop Attractions:\n- Gateway of India\n- Marine Drive, Juhu Beach\n- Elephanta Caves\n- Film City, Colaba\n\nBest Time: Oct-Feb (18-32C)\nStay: 500-100000/night", quickReplies: ['Hotels in Mumbai', 'Things to do', 'Mumbai weather']};
            }
            
            if (message.indexOf('goa') !== -1) {
                return {text: "GOA - Beach Paradise\n\nTop Attractions:\n- Baga Beach, Calangute\n- Old Goa Churches\n- Palolem Beach\n- Dudhsagar Falls\n\nBest Time: Nov-Feb (22-32C)\nStay: 500-25000/night", quickReplies: ['Hotels in Goa', 'Things to do', 'Goa weather']};
            }
            
            if (message.indexOf('jaipur') !== -1) {
                return {text: "JAIPUR - Pink City\n\nTop Attractions:\n- Amber Fort, Hawa Mahal\n- City Palace, Jantar Mantar\n- Nahargarh Fort\n- Local markets\n\nBest Time: Oct-Mar (10-30C)\nStay: 500-30000/night", quickReplies: ['Hotels in Jaipur', 'Things to do', 'Jaipur weather']};
            }
            
            if (message.indexOf('agra') !== -1 || message.indexOf('taj') !== -1) {
                return {text: "AGRA - Home of Taj Mahal\n\nTop Attractions:\n- Taj Mahal (must visit!)\n- Agra Fort\n- Fatehpur Sikri\n- Tomb of Itimad-ud-Daulah\n\nBest Time: Oct-Mar (10-30C)\nStay: 500-20000/night", quickReplies: ['Hotels in Agra', 'Things to do', 'Agra weather']};
            }
            
            if (message.indexOf('kerala') !== -1) {
                return {text: "KERALA - God's Own Country\n\nTop Attractions:\n- Backwaters of Alleppey\n- Hill station of Munnar\n- Wayanad wildlife\n- Kochi heritage\n\nBest Time: Sep-Mar (24-33C)\nStay: 500-35000/night", quickReplies: ['Hotels in Kerala', 'Things to do', 'Kerala weather']};
            }
            
            if (message.indexOf('ladakh') !== -1) {
                return {text: "LADAKH - Land of High Passes\n\nTop Attractions:\n- Pangong Lake\n- Nubra Valley\n- Khardungla Pass\n- Ancient monasteries\n\nBest Time: May-Sep (10-25C)\nStay: 500-15000/night", quickReplies: ['Hotels in Ladakh', 'Things to do', 'Ladakh weather']};
            }
            
            if (message.indexOf('varanasi') !== -1) {
                return {text: "VARANASI - Spiritual Capital\n\nTop Attractions:\n- Ganga Aarti at Dasaswamedh Ghat\n- Kashi Vishwanath Temple\n- Sarnath Buddhist site\n- Boat ride on Ganges\n\nBest Time: Oct-Mar (15-32C)\nStay: 500-15000/night", quickReplies: ['Hotels in Varanasi', 'Things to do', 'Varanasi weather']};
            }
            
            if (message.indexOf('hello') !== -1 || message.indexOf('hi') !== -1 || message.indexOf('hey') !== -1) {
                return {text: "Hello! Welcome to TourGuide Pro! How can I assist you with your travel plans today?", quickReplies: ['Book a hotel', 'Find destinations', 'Plan my trip']};
            }
            
            if (message.indexOf('thank') !== -1) {
                return {text: "You're welcome! Have a wonderful trip! Feel free to ask if you need any more help.", quickReplies: ['Book a hotel', 'Find destinations', 'Start a new trip']};
            }
            
            return {text: "I'd be happy to help with your travel plans! Ask me about:\n- Hotels\n- Destinations\n- Trip planning\n- Cab booking\n- Weather\n- Budget\n- Food", quickReplies: ['Hotels', 'Destinations', 'Plan my trip']};
        }
    };
    tourGuideChatbot.init();
});
