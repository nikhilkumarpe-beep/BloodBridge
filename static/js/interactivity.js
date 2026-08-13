// ===== INTERACTIVITY ENHANCEMENTS =====
// Phase 1: Sticky Header, Form Validation, AJAX Search, Tooltips

// ===== 1. STICKY HEADER =====
function initStickyHeader() {
    const header = document.querySelector('header');
    if (!header) return;

    let lastScroll = 0;
    const scrollThreshold = 100;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > scrollThreshold) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });
}

// ===== 2. DYNAMIC FORM VALIDATION =====
function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, select, textarea');

        inputs.forEach(input => {
            // Real-time validation on blur
            input.addEventListener('blur', () => validateField(input));

            // Clear error on focus
            input.addEventListener('focus', () => clearFieldError(input));
        });

        // Prevent submission if invalid
        form.addEventListener('submit', (e) => {
            let isValid = true;
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
                showFormError(form, 'Please fix the errors before submitting.');
            }
        });
    });
}

function validateField(input) {
    const value = input.value.trim();
    const type = input.type;
    const name = input.name;
    let isValid = true;
    let errorMessage = '';

    // Required field check
    if (input.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required';
    }
    // Email validation
    else if (type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address';
        }
    }
    // Phone validation (Indian format)
    else if (name === 'phone' && value) {
        const phoneRegex = /^[6-9]\d{9}$/;
        if (!phoneRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid 10-digit mobile number';
        }
    }
    // Password strength
    else if (type === 'password' && value && value.length < 6) {
        isValid = false;
        errorMessage = 'Password must be at least 6 characters';
    }
    // Age validation
    else if (name === 'age' && value) {
        const age = parseInt(value);
        if (age < 18 || age > 65) {
            isValid = false;
            errorMessage = 'Age must be between 18 and 65';
        }
    }

    if (isValid) {
        showFieldSuccess(input);
    } else {
        showFieldError(input, errorMessage);
    }

    return isValid;
}

function showFieldError(input, message) {
    clearFieldError(input);

    input.classList.add('error');
    input.classList.remove('success');

    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        color: #d32f2f;
        font-size: 0.875rem;
        margin-top: 4px;
        animation: slideDown 0.3s ease-out;
    `;

    input.parentElement.appendChild(errorDiv);
}

function showFieldSuccess(input) {
    clearFieldError(input);
    input.classList.add('success');
    input.classList.remove('error');
}

function clearFieldError(input) {
    input.classList.remove('error', 'success');
    const existingError = input.parentElement.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
}

function showFormError(form, message) {
    const existingError = form.querySelector('.form-error');
    if (existingError) existingError.remove();

    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error';
    errorDiv.textContent = message;
    errorDiv.style.cssText = `
        background: #ffebee;
        color: #d32f2f;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 4px solid #d32f2f;
        animation: slideDown 0.3s ease-out;
    `;

    form.insertBefore(errorDiv, form.firstChild);
}

// ===== 3. AJAX SEARCH =====
function initAjaxSearch() {
    const searchForm = document.querySelector('#donorSearchForm');
    if (!searchForm) return;

    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(searchForm);
        const params = new URLSearchParams(formData);

        // Show loading state
        showSearchLoading();

        try {
            const response = await fetch(`/api/search-donors?${params}`);
            const data = await response.json();

            if (data.success) {
                displaySearchResults(data.donors);
            } else {
                showSearchError(data.message || 'Search failed');
            }
        } catch (error) {
            showSearchError('Network error. Please try again.');
        }
    });
}

function showSearchLoading() {
    const resultsContainer = document.querySelector('#searchResults');
    if (!resultsContainer) return;

    resultsContainer.innerHTML = `
        <div class="search-loading" style="text-align: center; padding: 40px;">
            <div class="spinner" style="
                width: 50px;
                height: 50px;
                border: 5px solid #f3f3f3;
                border-top: 5px solid #d32f2f;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto 20px;
            "></div>
            <p>Searching for donors...</p>
        </div>
    `;
}

function displaySearchResults(donors) {
    const resultsContainer = document.querySelector('#searchResults');
    if (!resultsContainer) return;

    if (donors.length === 0) {
        resultsContainer.innerHTML = `
            <div class="no-results" style="text-align: center; padding: 40px;">
                <i class="fas fa-search" style="font-size: 3rem; color: #bdc3c7; margin-bottom: 20px;"></i>
                <h3>No donors found</h3>
                <p>Try adjusting your search criteria</p>
            </div>
        `;
        return;
    }

    resultsContainer.innerHTML = donors.map((donor, index) => `
        <div class="donor-card fade-in" style="animation-delay: ${index * 0.1}s;">
            <!-- Donor card content -->
        </div>
    `).join('');
}

function showSearchError(message) {
    const resultsContainer = document.querySelector('#searchResults');
    if (!resultsContainer) return;

    resultsContainer.innerHTML = `
        <div class="search-error" style="
            background: #ffebee;
            color: #d32f2f;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        ">
            <i class="fas fa-exclamation-circle" style="font-size: 2rem; margin-bottom: 10px;"></i>
            <p>${message}</p>
        </div>
    `;
}

// ===== 4. INTERACTIVE TOOLTIPS =====
function initTooltips() {
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');

    tooltipTriggers.forEach(trigger => {
        const tooltipText = trigger.getAttribute('data-tooltip');

        trigger.addEventListener('mouseenter', (e) => {
            showTooltip(e.target, tooltipText);
        });

        trigger.addEventListener('mouseleave', () => {
            hideTooltip();
        });

        // Mobile support
        trigger.addEventListener('click', (e) => {
            if (window.innerWidth < 768) {
                e.preventDefault();
                showTooltip(e.target, tooltipText);
                setTimeout(hideTooltip, 3000);
            }
        });
    });
}

function showTooltip(element, text) {
    hideTooltip(); // Remove any existing tooltip

    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    tooltip.style.cssText = `
        position: absolute;
        background: #2c3e50;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.875rem;
        z-index: 10000;
        pointer-events: none;
        animation: fadeIn 0.2s ease-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;

    document.body.appendChild(tooltip);

    const rect = element.getBoundingClientRect();
    tooltip.style.top = (rect.top - tooltip.offsetHeight - 8) + 'px';
    tooltip.style.left = (rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)) + 'px';
}

function hideTooltip() {
    const tooltip = document.querySelector('.tooltip');
    if (tooltip) {
        tooltip.remove();
    }
}

// ===== INITIALIZE ALL =====
document.addEventListener('DOMContentLoaded', () => {
    initStickyHeader();
    initFormValidation();
    initAjaxSearch();
    initTooltips();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    input.error, select.error, textarea.error {
        border-color: #d32f2f !important;
        background-color: #ffebee !important;
    }

    input.success, select.success, textarea.success {
        border-color: #4caf50 !important;
        background-color: #f1f8f4 !important;
    }
`;
document.head.appendChild(style);
