// DOM Elements
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');
const navLinksItems = document.querySelectorAll('.nav-links li a');

// Mobile Menu Toggle
if (hamburger) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navLinks.classList.toggle('active');
    });
}

// Close mobile menu when clicking on a nav link
navLinksItems.forEach(link => {
    link.addEventListener('click', () => {
        if (navLinks.classList.contains('active')) {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
        }
    });
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});

// Form Validation for Donor Registration
const donorForm = document.getElementById('donorForm');
if (donorForm) {
    donorForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Reset previous errors
        resetErrors();
        
        // Validate form fields
        let isValid = true;
        const formData = {};
        
        // Required fields validation
        const requiredFields = ['fullName', 'email', 'phone', 'bloodGroup', 'dob', 'address', 'city', 'state', 'zipCode'];
        requiredFields.forEach(field => {
            const input = document.getElementById(field);
            if (!input.value.trim()) {
                showError(input, 'This field is required');
                isValid = false;
            } else {
                formData[field] = input.value.trim();
            }
        });
        
        // Email validation
        const email = document.getElementById('email');
        if (email.value && !isValidEmail(email.value)) {
            showError(email, 'Please enter a valid email address');
            isValid = false;
        }
        
        // Phone validation
        const phone = document.getElementById('phone');
        if (phone.value && !isValidPhone(phone.value)) {
            showError(phone, 'Please enter a valid phone number');
            isValid = false;
        }
        
        // If form is valid, save to localStorage
        if (isValid) {
            // Get existing donors or initialize empty array
            const existingDonors = JSON.parse(localStorage.getItem('donors') || '[]');
            
            // Add new donor
            existingDonors.push({
                id: Date.now(),
                ...formData,
                registrationDate: new Date().toISOString(),
                lastDonationDate: null,
                isAvailable: true
            });
            
            // Save to localStorage
            localStorage.setItem('donors', JSON.stringify(existingDonors));
            
            // Show success message
            showAlert('Donor registration successful! Thank you for your contribution.', 'success');
            
            // Reset form
            donorForm.reset();
            
            // Redirect to home page after 2 seconds
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
        }
    });
}

// Form Validation for Blood Request
const requestForm = document.getElementById('requestForm');
if (requestForm) {
    requestForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        resetErrors();
        let isValid = true;
        const formData = {};
        
        // Required fields validation
        const requiredFields = ['patientName', 'bloodGroup', 'unitsRequired', 'hospitalName', 'doctorName', 'contactPerson', 'contactPhone', 'hospitalAddress', 'city', 'requiredDate'];
        requiredFields.forEach(field => {
            const input = document.getElementById(field);
            if (!input.value.trim()) {
                showError(input, 'This field is required');
                isValid = false;
            } else {
                formData[field] = input.value.trim();
            }
        });
        
        // Phone validation
        const contactPhone = document.getElementById('contactPhone');
        if (contactPhone.value && !isValidPhone(contactPhone.value)) {
            showError(contactPhone, 'Please enter a valid phone number');
            isValid = false;
        }
        
        // If form is valid, save to localStorage
        if (isValid) {
            // Get existing requests or initialize empty array
            const existingRequests = JSON.parse(localStorage.getItem('bloodRequests') || '[]');
            
            // Add new request
            existingRequests.push({
                id: Date.now(),
                ...formData,
                requestDate: new Date().toISOString(),
                status: 'Pending'
            });
            
            // Save to localStorage
            localStorage.setItem('bloodRequests', JSON.stringify(existingRequests));
            
            // Show success message
            showAlert('Blood request submitted successfully! We will contact you soon.', 'success');
            
            // Reset form
            requestForm.reset();
        }
    });
}

// Contact Form
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        resetErrors();
        let isValid = true;
        
        // Required fields validation
        const requiredFields = ['name', 'email', 'subject', 'message'];
        requiredFields.forEach(field => {
            const input = document.getElementById(field);
            if (!input.value.trim()) {
                showError(input, 'This field is required');
                isValid = false;
            }
        });
        
        // Email validation
        const email = document.getElementById('email');
        if (email.value && !isValidEmail(email.value)) {
            showError(email, 'Please enter a valid email address');
            isValid = false;
        }
        
        if (isValid) {
            // In a real app, you would send this data to a server
            showAlert('Thank you for your message! We will get back to you soon.', 'success');
            contactForm.reset();
        }
    });
}

// Search Functionality for Donors
const searchForm = document.getElementById('searchForm');
if (searchForm) {
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const bloodGroup = document.getElementById('searchBloodGroup').value;
        const city = document.getElementById('searchCity').value.toLowerCase();
        
        // Get all donors from localStorage
        const donors = JSON.parse(localStorage.getItem('donors') || '[]');
        
        // Filter donors based on search criteria
        const filteredDonors = donors.filter(donor => {
            const matchesBloodGroup = !bloodGroup || donor.bloodGroup === bloodGroup;
            const matchesCity = !city || donor.city.toLowerCase().includes(city);
            return matchesBloodGroup && matchesCity && donor.isAvailable;
        });
        
        // Display results
        displaySearchResults(filteredDonors);
    });
}

// Display search results
function displaySearchResults(donors) {
    const resultsContainer = document.getElementById('searchResults');
    
    if (!resultsContainer) return;
    
    if (donors.length === 0) {
        resultsContainer.innerHTML = '<div class="alert alert-info">No donors found matching your criteria.</div>';
        return;
    }
    
    let html = '<div class="search-results">';
    
    donors.forEach(donor => {
        html += `
            <div class="donor-card">
                <div class="donor-info">
                    <h4>${donor.fullName}</h4>
                    <p><i class="fas fa-tint"></i> Blood Group: <strong>${donor.bloodGroup}</strong></p>
                    <p><i class="fas fa-map-marker-alt"></i> ${donor.city}, ${donor.state}</p>
                    <p><i class="fas fa-phone"></i> ${donor.phone}</p>
                    <p><i class="fas fa-envelope"></i> ${donor.email}</p>
                </div>
                <div class="donor-actions">
                    <a href="#" class="btn btn-primary request-blood" data-donor-id="${donor.id}">Request Blood</a>
                    <a href="tel:${donor.phone}" class="btn btn-secondary"><i class="fas fa-phone"></i> Call Now</a>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    resultsContainer.innerHTML = html;
    
    // Add event listeners to request blood buttons
    document.querySelectorAll('.request-blood').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const donorId = this.getAttribute('data-donor-id');
            // In a real app, you would redirect to a request form or show a modal
            window.location.href = `request.html?donorId=${donorId}`;
        });
    });
}

// Initialize Blood Bank Inventory
function initBloodBankInventory() {
    const bloodTypes = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];
    const inventoryContainer = document.getElementById('bloodInventory');
    
    if (!inventoryContainer) return;
    
    // Get inventory from localStorage or initialize with default values
    let inventory = JSON.parse(localStorage.getItem('bloodInventory'));
    
    if (!inventory) {
        // Initialize with random values for demo
        inventory = bloodTypes.map(type => ({
            bloodType: type,
            units: Math.floor(Math.random() * 20) + 5, // Random units between 5-25
            lastUpdated: new Date().toISOString()
        }));
        
        localStorage.setItem('bloodInventory', JSON.stringify(inventory));
    }
    
    // Update stats
    updateBloodStats(inventory);
    
    // Create inventory table
    let html = `
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Blood Type</th>
                        <th>Available Units</th>
                        <th>Status</th>
                        <th>Last Updated</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    inventory.forEach(item => {
        const status = item.units < 5 ? 'Low' : item.units < 15 ? 'Medium' : 'Good';
        const statusClass = status.toLowerCase();
        
        html += `
            <tr>
                <td>${item.bloodType}</td>
                <td>${item.units} units</td>
                <td><span class="status-badge ${statusClass}">${status}</span></td>
                <td>${formatDate(item.lastUpdated)}</td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
    `;
    
    inventoryContainer.innerHTML = html;
}

// Update blood statistics
function updateBloodStats(inventory) {
    const statsContainer = document.querySelector('.blood-stats');
    if (!statsContainer) return;
    
    const totalUnits = inventory.reduce((sum, item) => sum + item.units, 0);
    const lowStock = inventory.filter(item => item.units < 5).length;
    const criticalTypes = inventory
        .filter(item => item.units < 3)
        .map(item => item.bloodType)
        .join(', ');
    
    statsContainer.innerHTML = `
        <div class="blood-stat-card">
            <i class="fas fa-tint"></i>
            <h3>${totalUnits}</h3>
            <p>Total Units Available</p>
        </div>
        <div class="blood-stat-card">
            <i class="fas fa-heartbeat"></i>
            <h3>${inventory.length - lowStock}/${inventory.length}</h3>
            <p>Blood Types in Stock</p>
        </div>
        <div class="blood-stat-card">
            <i class="fas fa-exclamation-triangle"></i>
            <h3>${lowStock}</h3>
            <p>Low Stock Types</p>
        </div>
        <div class="blood-stat-card">
            <i class="fas fa-exclamation-circle"></i>
            <h3>${criticalTypes || 'None'}</h3>
            <p>Critical Stock</p>
        </div>
    `;
}

// Helper Functions
function showError(input, message) {
    const formGroup = input.closest('.form-group');
    if (!formGroup) return;
    
    // Remove existing error if any
    const existingError = formGroup.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Add error class to input
    input.classList.add('error');
    
    // Create and append error message
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.style.color = '#dc3545';
    errorElement.style.fontSize = '0.875rem';
    errorElement.style.marginTop = '5px';
    errorElement.textContent = message;
    
    formGroup.appendChild(errorElement);
}

function resetErrors() {
    // Remove all error messages
    document.querySelectorAll('.error-message').forEach(el => el.remove());
    
    // Remove error class from all inputs
    document.querySelectorAll('.error').forEach(el => {
        el.classList.remove('error');
    });
}

function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    // Insert alert at the top of the form
    const form = document.querySelector('form');
    if (form) {
        form.insertBefore(alertDiv, form.firstChild);
    } else {
        // If no form, insert at the top of the content area
        const content = document.querySelector('.content') || document.querySelector('main');
        if (content) {
            content.insertBefore(alertDiv, content.firstChild);
        } else {
            document.body.insertBefore(alertDiv, document.body.firstChild);
        }
    }
    
    // Auto-remove alert after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function isValidPhone(phone) {
    const re = /^[0-9\-\+\(\)\s]{10,20}$/;
    return re.test(phone);
}

function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Initialize page-specific functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize blood bank inventory on inventory page
    if (document.getElementById('bloodInventory')) {
        initBloodBankInventory();
    }
    
    // Initialize search form with blood type options
    const bloodGroupSelect = document.getElementById('searchBloodGroup');
    if (bloodGroupSelect) {
        const bloodTypes = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];
        bloodTypes.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            bloodGroupSelect.appendChild(option);
        });
    }
    
    // Initialize Google Maps on contact page
    if (document.getElementById('map')) {
        initMap();
    }
});

// Google Maps initialization
function initMap() {
    // This is a placeholder. In a real app, you would initialize the Google Map here.
    // You would need to include the Google Maps JavaScript API with your API key.
    // For the demo, we'll just show a placeholder.
    const mapContainer = document.getElementById('map');
    if (mapContainer) {
        mapContainer.innerHTML = `
            <div style="width: 100%; height: 100%; background: #f0f0f0; display: flex; justify-content: center; align-items: center; border-radius: 10px;">
                <div style="text-align: center; padding: 20px;">
                    <i class="fas fa-map-marker-alt" style="font-size: 3rem; color: #e63946; margin-bottom: 15px;"></i>
                    <h3>Our Location</h3>
                    <p>123 Health Street, City, Country</p>
                    <p>In a real application, this would display an interactive Google Map.</p>
                </div>
            </div>
        `;
    }
}

// Add smooth scrolling to all links
$(document).ready(function(){
    // Add smooth scrolling to all links
    $("a").on('click', function(event) {
        // Make sure this.hash has a value before overriding default behavior
        if (this.hash !== "") {
            // Prevent default anchor click behavior
            event.preventDefault();

            // Store hash
            var hash = this.hash;

            // Using jQuery's animate() method to add smooth page scroll
            // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
            $('html, body').animate({
                scrollTop: $(hash).offset().top - 80
            }, 800, function(){
                // Add hash (#) to URL when done scrolling (default click behavior)
                window.location.hash = hash;
            });
        }
    });
});
