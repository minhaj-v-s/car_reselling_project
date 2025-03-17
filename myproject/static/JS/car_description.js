// Initialize AOS (Animate on Scroll)
document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS
    AOS.init({
        duration: 1000,
        once: true,
        mirror: false
    });

    // DOM Elements
    const mainCarImage = document.getElementById('mainCarImage');
    const thumbnailButtons = document.querySelectorAll('.thumbnail-button');
    const nextButton = document.getElementById('prevButton');
    const prevButton = document.getElementById('nextButton');
    const whatsappButton = document.getElementById('whatsappButton');
    const whatsappPopup = document.getElementById('whatsappPopup');
    const closePopupButton = document.getElementById('closePopupButton');
    const lightbox = document.getElementById('lightbox');
    const lightboxImage = document.getElementById('lightboxImage');
    const closeLightboxButton = document.getElementById('closeLightboxButton');
    const specsContainer = document.getElementById('specsContainer');
    const specItems = document.querySelectorAll('.spec-item');
    
    // Variables
    let activeSlide = 0;
    let imageUrls = [];
    
    // Collect all image URLs
    thumbnailButtons.forEach(button => {
        const img = button.querySelector('img');
        if (img) {
            imageUrls.push(img.src);
        }
    });
    
    // Functions
    function setActiveSlide(index) {
        activeSlide = index;
        mainCarImage.src = imageUrls[index];
        
        thumbnailButtons.forEach((button, i) => {
            if (i === index) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });
    }
    
    function nextSlide() {
        let newIndex = activeSlide + 1;
        if (newIndex >= imageUrls.length) {
            newIndex = 0;
        }
        setActiveSlide(newIndex);
    }
    
    function prevSlide() {
        let newIndex = activeSlide - 1;
        if (newIndex < 0) {
            newIndex = imageUrls.length - 1;
        }
        setActiveSlide(newIndex);
    }
    
    function openWhatsAppPopup() {
        whatsappPopup.classList.add('active');
        
        // Generate QR code
        const qrCodeContainer = document.getElementById('qrCodeContainer');
        qrCodeContainer.innerHTML = ''; // Clear previous QR code
        
        const openWhatsAppLink = document.getElementById('openWhatsAppLink');
        const whatsappUrl = openWhatsAppLink.href;
        
        // Create QR code
        new QRCode(qrCodeContainer, {
            text: whatsappUrl,
            width: 180,
            height: 180,
            colorDark: "#000000",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.H
        });
    }
    
    function closeWhatsAppPopup() {
        whatsappPopup.classList.remove('active');
    }
    
    function openLightbox(imageUrl) {
        lightboxImage.src = imageUrl;
        lightbox.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
    
    function closeLightbox() {
        lightbox.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
    
    // Create Intersection Observer for specs animation
    function setupSpecsObserver() {
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                specItems.forEach((item, index) => {
                    setTimeout(() => {
                        item.classList.add('show');
                    }, index * 100);
                });
                observer.disconnect();
            }
        }, { threshold: 0.5 });
        
        if (specsContainer) {
            observer.observe(specsContainer);
        }
    }
    
    // Event Listeners
    nextButton.addEventListener('click', nextSlide);
    prevButton.addEventListener('click', prevSlide);
    
    thumbnailButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            setActiveSlide(index);
        });
    });
    
    mainCarImage.addEventListener('click', () => {
        openLightbox(mainCarImage.src);
    });
    
    whatsappButton.addEventListener('click', openWhatsAppPopup);
    closePopupButton.addEventListener('click', closeWhatsAppPopup);
    closeLightboxButton.addEventListener('click', closeLightbox);
    
    // Close lightbox when clicking outside the image
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (lightbox.style.display === 'flex') {
            if (e.key === 'Escape') {
                closeLightbox();
            }
        } else {
            if (e.key === 'ArrowLeft') {
                prevSlide();
            } else if (e.key === 'ArrowRight') {
                nextSlide();
            } else if (e.key === 'Escape' && whatsappPopup.classList.contains('active')) {
                closeWhatsAppPopup();
            }
        }
    });
    
    // Initialize
    setupSpecsObserver();
});