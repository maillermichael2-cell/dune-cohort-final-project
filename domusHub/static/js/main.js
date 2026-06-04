
function start(){
    console.log('DomusHub Initialized')
}

function toggleDiv(){
    const div = document.getElementById('sideBar')
    if (div.style.display === 'none' || div.style.display === ''){
        div.style.display = 'flex';
    }else{
        div.style.display = 'none';
    }
}




/**
 * ==========================================================================
 * DOMUSHUB PROPERTY EDIT AUTO CAROUSEL ENGINE
 * Handles self-sliding thumbnail gallery previews for listing management
 * ==========================================================================
 */

let autoSlideIndex = 0;
let autoPlayTimer = null;

function initAutoCarousel() {
    const viewport = document.getElementById('autoCarouselViewport');
    const slides = document.querySelectorAll('.edit-auto-carousel-slide');
    
    // Safety exit: Stop if the property edit carousel elements aren't on this page
    if (!viewport || slides.length <= 1) return;

    // Start 3-second infinite auto sliding loop
    startAutoPlay();

    // Pause sliding on hover so the agent can focus on form input elements comfortably
    const container = document.querySelector('.edit-auto-carousel-container');
    if (container) {
        container.addEventListener('mouseenter', stopAutoPlay);
        container.addEventListener('mouseleave', startAutoPlay);
    }
}

function moveAutoCarousel(direction) {
    const viewport = document.getElementById('autoCarouselViewport');
    const slides = document.querySelectorAll('.edit-auto-carousel-slide');
    const totalSlides = slides.length;
    
    if (!viewport || totalSlides <= 1) return;

    autoSlideIndex += direction;

    // Handle loops seamlessly
    if (autoSlideIndex >= totalSlides) autoSlideIndex = 0;
    if (autoSlideIndex < 0) autoSlideIndex = totalSlides - 1;

    // Glides the frame deck horizontally smoothly
    viewport.style.transform = `translateX(-${autoSlideIndex * 100}%)`;
}

function startAutoPlay() {
    if (!autoPlayTimer) {
        autoPlayTimer = setInterval(() => {
            moveAutoCarousel(1);
        }, 3000); 
    }
}

function stopAutoPlay() {
    if (autoPlayTimer) {
        clearInterval(autoPlayTimer);
        autoPlayTimer = null;
    }
}

// 🌟 CRITICAL FIX: Explicitly bind the function to the global window scope 
// This allows the HTML onclick attribute to find and execute the method immediately
window.moveAutoCarousel = moveAutoCarousel;

// Bootstrap initialization immediately when DOM elements render
document.addEventListener('DOMContentLoaded', initAutoCarousel);




/**
 * ==========================================================================
 * DOMUSHUB PUBLIC PROPERTY DETAIL AUTO CAROUSEL ENGINE
 * Handles infinite 3-second loop transitions for listing displays
 * ==========================================================================
 */

let currentSlideIndex = 0;
let detailPlayTimer = null;

function initDetailCarousel() {
    const viewport = document.getElementById('carouselViewport');
    const slides = document.querySelectorAll('.carousel-slide');
    
    // Safety exit: Stop if the property detail elements aren't on this page or there's only 1 image
    if (!viewport || slides.length <= 1) return;

    // Start 3-second infinite auto sliding loop
    startDetailAutoPlay();

    // Pause sliding on hover so the user can look closer at individual room details
    const container = document.querySelector('.carousel-container');
    if (container) {
        container.addEventListener('mouseenter', stopDetailAutoPlay);
        container.addEventListener('mouseleave', startDetailAutoPlay);
    }
}

function moveCarousel(direction) {
    const viewport = document.getElementById('carouselViewport');
    const slides = document.querySelectorAll('.carousel-slide');
    const totalSlides = slides.length;
    
    if (!viewport || totalSlides <= 1) return;

    currentSlideIndex += direction;

    // Endless loop wrapper handling parameters
    if (currentSlideIndex >= totalSlides) currentSlideIndex = 0;
    if (currentSlideIndex < 0) currentSlideIndex = totalSlides - 1;

    // Translates the slide deck canvas horizontal width dimensions smoothly
    viewport.style.transform = `translateX(-${currentSlideIndex * 100}%)`;
}

function startDetailAutoPlay() {
    if (!detailPlayTimer) {
        detailPlayTimer = setInterval(() => {
            moveCarousel(1);
        }, 3000); 
    }
}

function stopDetailAutoPlay() {
    if (detailPlayTimer) {
        clearInterval(detailPlayTimer);
        detailPlayTimer = null;
    }
}

// 🌟 CRITICAL GLOBAL WINDOW SCOPE BINDING 
// Allows the HTML onclick attribute to find and execute the method instantly from outside
window.moveCarousel = moveCarousel;

// Bootstrap initialization immediately when DOM elements render into view context
document.addEventListener('DOMContentLoaded', initDetailCarousel);

