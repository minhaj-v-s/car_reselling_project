/**
 * Car Description Page JavaScript
 * Enhanced user interactions for the car details page
 */

document.addEventListener('DOMContentLoaded', function() {
    // Image gallery behavior
    const carouselItems = document.querySelectorAll('.carousel-item img');
    
    carouselItems.forEach(item => {
        item.addEventListener('mouseover', function() {
            this.style.transform = 'scale(1.03)';
            this.style.transition = 'transform 0.5s ease';
        });
        
        item.addEventListener('mouseout', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Animate specifications on scroll
    const specs = document.querySelectorAll('.spec-item');
    
    function animateSpecs() {
        specs.forEach((spec, index) => {
            setTimeout(() => {
                spec.style.opacity = '1';
                spec.style.transform = 'translateY(0)';
            }, 100 * index);
        });
    }
    
    // Set initial state
    specs.forEach(spec => {
        spec.style.opacity = '0';
        spec.style.transform = 'translateY(20px)';
        spec.style.transition = 'all 0.5s ease';
    });
    
    // Call animation when element is in viewport
    const specsContainer = document.querySelector('.car-specs');
    
    if (specsContainer) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateSpecs();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(specsContainer);
    }
    
    // Button hover effects
    const buttons = document.querySelectorAll('.appointment-btn, .chat-btn');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-3px)';
            this.style.boxShadow = '0 7px 20px rgba(0, 0, 0, 0.15)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
        });
    });
    
    // Chat popup functionality - Simplified version
    const chatPopup = document.getElementById('chatPopup');
    const openChatBtn = document.getElementById('openChat');
    const closeChatBtn = document.querySelector('.close-chat-btn');
    
    if (openChatBtn && chatPopup) {
        openChatBtn.addEventListener('click', function() {
            chatPopup.style.display = 'block';
            chatPopup.style.animation = 'slideUp 0.4s ease-out forwards';
        });
    }
    
    if (closeChatBtn) {
        closeChatBtn.addEventListener('click', function() {
            chatPopup.style.display = 'none';
        });
    }
});
