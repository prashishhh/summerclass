// ===== HOMEPAGE INTERACTIONS & ANIMATIONS =====

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== SCROLL ANIMATIONS =====
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe all animated elements
    document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right').forEach(el => {
        observer.observe(el);
    });

    // ===== SMOOTH SCROLLING =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ===== PARALLAX EFFECT FOR HERO SECTION =====
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        });
    }

    // ===== CATEGORY CARDS HOVER EFFECTS =====
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // ===== PRODUCT CARDS INTERACTIONS =====
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        // Add to cart button interaction
        const addToCartBtn = card.querySelector('.add-to-cart-btn');
        if (addToCartBtn) {
            addToCartBtn.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Add loading state
                const originalText = this.textContent;
                this.textContent = 'Adding...';
                this.disabled = true;
                
                // Simulate API call
                setTimeout(() => {
                    this.textContent = 'Added!';
                    this.style.background = '#10b981';
                    
                    setTimeout(() => {
                        this.textContent = originalText;
                        this.style.background = '#111827';
                        this.disabled = false;
                    }, 1500);
                }, 1000);
            });
        }
    });

    // ===== BANNER CAROUSEL ENHANCEMENTS =====
    const bannerCarousel = document.querySelector('#bannerCarousel');
    if (bannerCarousel) {
        // Auto-play with pause on hover
        let autoplayInterval;
        
        function startAutoplay() {
            autoplayInterval = setInterval(() => {
                const nextButton = bannerCarousel.querySelector('.carousel-control-next');
                if (nextButton) {
                    nextButton.click();
                }
            }, 5000);
        }
        
        function stopAutoplay() {
            clearInterval(autoplayInterval);
        }
        
        bannerCarousel.addEventListener('mouseenter', stopAutoplay);
        bannerCarousel.addEventListener('mouseleave', startAutoplay);
        
        // Start autoplay initially
        startAutoplay();
        
        // Add progress bar
        const progressBar = document.createElement('div');
        progressBar.className = 'carousel-progress';
        progressBar.style.cssText = `
            position: absolute;
            bottom: 0;
            left: 0;
            height: 4px;
            background: rgba(255, 255, 255, 0.8);
            width: 0%;
            transition: width 0.1s linear;
            z-index: 10;
        `;
        bannerCarousel.appendChild(progressBar);
        
        // Update progress bar
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 0.1;
            progressBar.style.width = progress + '%';
            
            if (progress >= 100) {
                progress = 0;
                progressBar.style.width = '0%';
            }
        }, 50);
    }

    // ===== SEARCH FUNCTIONALITY =====
    const searchInput = document.querySelector('.search-box input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const categoryCards = document.querySelectorAll('.category-card');
            
            categoryCards.forEach(card => {
                const categoryName = card.querySelector('.category-info h3').textContent.toLowerCase();
                if (categoryName.includes(searchTerm)) {
                    card.style.display = 'block';
                    card.style.opacity = '1';
                } else {
                    card.style.opacity = '0.5';
                }
            });
        });
    }

    // ===== FILTER PILLS FUNCTIONALITY =====
    const filterPills = document.querySelectorAll('.filter-pill');
    filterPills.forEach(pill => {
        pill.addEventListener('click', function() {
            // Remove active class from all pills
            filterPills.forEach(p => p.classList.remove('active'));
            
            // Add active class to clicked pill
            this.classList.add('active');
            
            // Get filter value
            const filterValue = this.getAttribute('data-filter');
            
            // Filter products (you can implement your own filtering logic here)
            filterProducts(filterValue);
        });
    });

    // ===== LAZY LOADING FOR IMAGES =====
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // ===== SCROLL TO TOP BUTTON =====
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.innerHTML = '↑';
    scrollToTopBtn.className = 'scroll-to-top';
    scrollToTopBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #111827;
        color: white;
        border: none;
        cursor: pointer;
        font-size: 20px;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    `;
    
    document.body.appendChild(scrollToTopBtn);
    
    // Show/hide scroll to top button
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollToTopBtn.style.opacity = '1';
            scrollToTopBtn.style.visibility = 'visible';
        } else {
            scrollToTopBtn.style.opacity = '0';
            scrollToTopBtn.style.visibility = 'hidden';
        }
    });
    
    // Scroll to top functionality
    scrollToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // ===== MOBILE MENU TOGGLE =====
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
            mobileMenuToggle.classList.toggle('active');
        });
    }

    // ===== PRODUCT QUICK VIEW =====
    const quickViewButtons = document.querySelectorAll('.quick-view-btn');
    quickViewButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.getAttribute('data-product-id');
            // Implement quick view modal here
            console.log('Quick view for product:', productId);
        });
    });

    // ===== WISHLIST FUNCTIONALITY =====
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    wishlistButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            this.classList.toggle('active');
            
            if (this.classList.contains('active')) {
                this.innerHTML = '❤️';
                this.style.color = '#ef4444';
            } else {
                this.innerHTML = '🤍';
                this.style.color = '#6b7280';
            }
        });
    });

    // ===== PERFORMANCE OPTIMIZATION =====
    // Debounce scroll events
    let scrollTimeout;
    window.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            // Handle scroll-based animations here
        }, 16); // 60fps
    });

    // ===== ACCESSIBILITY ENHANCEMENTS =====
    // Add keyboard navigation for category cards
    const focusableElements = document.querySelectorAll('.category-card, .product-card');
    focusableElements.forEach(element => {
        element.setAttribute('tabindex', '0');
        
        element.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });

    // ===== ANALYTICS & TRACKING =====
    // Track user interactions
    const trackEvent = (eventName, eventData) => {
        // Implement your analytics tracking here
        console.log('Event tracked:', eventName, eventData);
    };

    // Track category clicks
    document.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('click', () => {
            const categoryName = card.querySelector('.category-info h3').textContent;
            trackEvent('category_click', { category: categoryName });
        });
    });

    // Track product interactions
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const productCard = btn.closest('.product-card');
            const productName = productCard.querySelector('.product-name').textContent;
            trackEvent('add_to_cart', { product: productName });
        });
    });

    console.log('Homepage interactions loaded successfully!');
});

// ===== UTILITY FUNCTIONS =====

function filterProducts(filterValue) {
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        if (filterValue === 'all') {
            card.style.display = 'block';
            card.style.opacity = '1';
        } else {
            const productCategory = card.getAttribute('data-category');
            if (productCategory === filterValue) {
                card.style.display = 'block';
                card.style.opacity = '1';
            } else {
                card.style.display = 'none';
            }
        }
    });
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;
    
    // Set background color based on type
    switch(type) {
        case 'success':
            notification.style.background = '#10b981';
            break;
        case 'error':
            notification.style.background = '#ef4444';
            break;
        case 'warning':
            notification.style.background = '#f59e0b';
            break;
        default:
            notification.style.background = '#3b82f6';
    }
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}


