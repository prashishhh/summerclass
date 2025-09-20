// ===== MODERN DESIGN INTERACTIONS FOR ALL PAGES =====

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

    // ===== ENHANCED FORM INTERACTIONS =====
    const formControls = document.querySelectorAll('.form-control');
    formControls.forEach(control => {
        // Add floating label effect
        if (control.value) {
            control.classList.add('has-value');
        }
        
        control.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        control.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            if (this.value) {
                this.classList.add('has-value');
            } else {
                this.classList.remove('has-value');
            }
        });
        
        control.addEventListener('input', function() {
            if (this.value) {
                this.classList.add('has-value');
            } else {
                this.classList.remove('has-value');
            }
        });
    });

    // ===== ENHANCED BUTTON INTERACTIONS =====
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
        
        button.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(0)';
        });
        
        button.addEventListener('mouseup', function() {
            this.style.transform = 'translateY(-2px)';
        });
    });

    // ===== ENHANCED CARD INTERACTIONS =====
    const cards = document.querySelectorAll('.card, .card-product-grid');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // ===== ENHANCED TABLE INTERACTIONS =====
    const tableRows = document.querySelectorAll('.table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.background = 'var(--bg-secondary)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.background = '';
        });
    });

    // ===== ENHANCED NAVIGATION =====
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.background = 'var(--bg-secondary)';
        });
        
        link.addEventListener('mouseleave', function() {
            if (!this.classList.contains('active')) {
                this.style.background = '';
            }
        });
    });

    // ===== ENHANCED FILTER INTERACTIONS =====
    const filterHeaders = document.querySelectorAll('.filter-group .card-header a');
    filterHeaders.forEach(header => {
        header.addEventListener('click', function(e) {
            const icon = this.querySelector('.icon-control');
            if (icon) {
                icon.style.transition = 'transform 0.2s ease';
            }
        });
    });

    // ===== ENHANCED CHECKBOX BUTTONS =====
    const checkboxBtns = document.querySelectorAll('.checkbox-btn input[type="checkbox"]');
    checkboxBtns.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const btn = this.nextElementSibling;
            if (this.checked) {
                btn.style.background = 'var(--accent-color)';
                btn.style.color = 'white';
                btn.style.borderColor = 'var(--accent-color)';
            } else {
                btn.style.background = 'var(--bg-tertiary)';
                btn.style.color = 'var(--text-secondary)';
                btn.style.borderColor = 'var(--border-color)';
            }
        });
    });

    // ===== ENHANCED PAGINATION =====
    const pageLinks = document.querySelectorAll('.page-link');
    pageLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-1px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // ===== ENHANCED PRODUCT IMAGES =====
    const productImages = document.querySelectorAll('.card-product-grid .img-wrap img, .gallery-wrap img');
    productImages.forEach(img => {
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // ===== ENHANCED ALERTS =====
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Add close button if not present
        if (!alert.querySelector('.close')) {
            const closeBtn = document.createElement('button');
            closeBtn.type = 'button';
            closeBtn.className = 'close';
            closeBtn.innerHTML = '&times;';
            closeBtn.style.cssText = `
                background: none;
                border: none;
                font-size: 1.5rem;
                font-weight: bold;
                line-height: 1;
                color: inherit;
                opacity: 0.5;
                cursor: pointer;
                float: right;
                margin-left: 1rem;
            `;
            
            closeBtn.addEventListener('click', function() {
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            });
            
            alert.appendChild(closeBtn);
        }
    });

    // ===== ENHANCED DROPDOWNS =====
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (toggle && menu) {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                menu.classList.toggle('show');
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function(e) {
                if (!dropdown.contains(e.target)) {
                    menu.classList.remove('show');
                }
            });
        }
    });

    // ===== ENHANCED MODALS =====
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            this.style.opacity = '0';
            setTimeout(() => {
                this.style.opacity = '1';
            }, 10);
        });
        
        modal.addEventListener('hide.bs.modal', function() {
            this.style.opacity = '0';
        });
    });

    // ===== ENHANCED TOOLTIPS =====
    const tooltipElements = document.querySelectorAll('[data-toggle="tooltip"]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'custom-tooltip';
            tooltip.textContent = this.getAttribute('title');
            tooltip.style.cssText = `
                position: absolute;
                background: var(--primary-color);
                color: white;
                padding: 8px 12px;
                border-radius: var(--radius-sm);
                font-size: 12px;
                font-weight: 500;
                z-index: 1000;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.2s ease;
            `;
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
            
            setTimeout(() => {
                tooltip.style.opacity = '1';
            }, 10);
            
            this._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });

    // ===== ENHANCED LOADING STATES =====
    const loadingElements = document.querySelectorAll('.skeleton');
    loadingElements.forEach(element => {
        // Add loading animation
        element.style.animation = 'loading 1.5s infinite';
    });

    // ===== ENHANCED ACCESSIBILITY =====
    // Add keyboard navigation for interactive elements
    const interactiveElements = document.querySelectorAll('.btn, .card, .nav-link, .page-link');
    interactiveElements.forEach(element => {
        element.setAttribute('tabindex', '0');
        
        element.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });

    // ===== ENHANCED PERFORMANCE =====
    // Debounce scroll events
    let scrollTimeout;
    window.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            // Handle scroll-based animations here
        }, 16); // 60fps
    });

    // ===== ENHANCED RESPONSIVENESS =====
    // Handle responsive behavior
    function handleResponsive() {
        const isMobile = window.innerWidth <= 768;
        
        if (isMobile) {
            document.body.classList.add('mobile');
        } else {
            document.body.classList.remove('mobile');
        }
    }
    
    window.addEventListener('resize', handleResponsive);
    handleResponsive(); // Initial call

    // ===== ENHANCED THEME SUPPORT =====
    // Check for system theme preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.body.classList.add('dark-theme');
    }
    
    // Listen for theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (e.matches) {
            document.body.classList.add('dark-theme');
        } else {
            document.body.classList.remove('dark-theme');
        }
    });

    // ===== ENHANCED ANALYTICS =====
    // Track user interactions
    const trackEvent = (eventName, eventData) => {
        // Implement your analytics tracking here
        console.log('Event tracked:', eventName, eventData);
    };

    // Track button clicks
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const buttonText = btn.textContent.trim();
            const buttonType = btn.className.includes('btn-primary') ? 'primary' : 'secondary';
            trackEvent('button_click', { text: buttonText, type: buttonType });
        });
    });

    // Track form submissions
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', () => {
            const formAction = form.action || 'unknown';
            trackEvent('form_submit', { action: formAction });
        });
    });

    // Track product interactions
    document.querySelectorAll('.card-product-grid').forEach(card => {
        card.addEventListener('click', () => {
            const productName = card.querySelector('.title')?.textContent || 'Unknown';
            trackEvent('product_click', { name: productName });
        });
    });

    console.log('Modern design interactions loaded successfully!');
});

// ===== UTILITY FUNCTIONS =====

// Smooth scroll to element
function smoothScrollTo(element, offset = 0) {
    const targetPosition = element.offsetTop - offset;
    window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
    });
}

// Add loading state to button
function setButtonLoading(button, isLoading, loadingText = 'Loading...') {
    if (isLoading) {
        button.disabled = true;
        button.dataset.originalText = button.textContent;
        button.textContent = loadingText;
        button.classList.add('loading');
    } else {
        button.disabled = false;
        button.textContent = button.dataset.originalText || 'Submit';
        button.classList.remove('loading');
    }
}

// Show notification
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        border-radius: var(--radius-md);
        color: white;
        font-weight: 600;
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;
    
    // Set background color based on type
    const colors = {
        success: 'var(--success-color)',
        error: 'var(--danger-color)',
        warning: 'var(--warning-color)',
        info: 'var(--accent-color)'
    };
    
    notification.style.background = colors[type] || colors.info;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after duration
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, duration);
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

