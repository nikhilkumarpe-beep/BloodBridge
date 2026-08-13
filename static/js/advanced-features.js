// ===== Particle System =====
class ParticleSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.resize();
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
    }

    createParticle() {
        return {
            x: Math.random() * this.canvas.width,
            y: -10,
            size: Math.random() * 3 + 2,
            speed: Math.random() * 2 + 1,
            opacity: Math.random() * 0.5 + 0.3
        };
    }

    update() {
        // Add new particles
        if (this.particles.length < 50 && Math.random() < 0.1) {
            this.particles.push(this.createParticle());
        }

        // Update and draw particles
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];
            p.y += p.speed;

            // Draw blood drop shape
            this.ctx.save();
            this.ctx.translate(p.x, p.y);
            this.ctx.rotate(45 * Math.PI / 180);
            this.ctx.globalAlpha = p.opacity;
            this.ctx.fillStyle = '#e74c3c';
            this.ctx.beginPath();
            this.ctx.arc(0, 0, p.size, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.restore();

            // Remove off-screen particles
            if (p.y > this.canvas.height) {
                this.particles.splice(i, 1);
            }
        }

        requestAnimationFrame(() => this.update());
    }

    start() {
        this.update();
    }
}

// ===== Animated Counter =====
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target.toLocaleString();
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current).toLocaleString();
        }
    }, 16);
}

// ===== Progress Circle =====
function updateProgressCircle(circle, percentage) {
    const radius = circle.r.baseVal.value;
    const circumference = radius * 2 * Math.PI;
    const offset = circumference - (percentage / 100) * circumference;

    circle.style.strokeDasharray = `${circumference} ${circumference}`;
    circle.style.strokeDashoffset = offset;
}

// ===== Confetti Effect =====
function createConfetti() {
    const colors = ['#e74c3c', '#FF9933', '#138808', '#f39c12', '#3498db'];
    const confettiCount = 50;

    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.animationDelay = Math.random() * 3 + 's';
        confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
        document.body.appendChild(confetti);

        setTimeout(() => confetti.remove(), 5000);
    }
}

// ===== Toast Notification =====
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icon = type === 'success' ? 'fa-check-circle' :
        type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle';

    toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <span>${message}</span>
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ===== Typing Effect =====
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.textContent = '';

    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }

    type();
}

// ===== Ripple Effect =====
function createRipple(event) {
    const button = event.currentTarget;
    const ripple = document.createElement('span');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.className = 'ripple';
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';

    button.appendChild(ripple);

    setTimeout(() => ripple.remove(), 600);
}

// ===== Scroll Reveal =====
function initScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('slide-up');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    // DISABLED: Scroll reveal was hiding content
    // document.querySelectorAll('.reveal-on-scroll').forEach(el => {
    //     el.style.opacity = '0';
    //     observer.observe(el);
    // });
}

// ===== Blood Drop Cursor Trail =====
let cursorTrail = [];
function initCursorTrail() {
    document.addEventListener('mousemove', (e) => {
        if (cursorTrail.length > 10) {
            const old = cursorTrail.shift();
            old.remove();
        }

        const drop = document.createElement('div');
        drop.className = 'cursor-blood-drop';
        drop.style.cssText = `
            position: fixed;
            width: 8px;
            height: 8px;
            background: var(--primary-color);
            border-radius: 50%;
            pointer-events: none;
            left: ${e.clientX}px;
            top: ${e.clientY}px;
            opacity: 0.6;
            transition: opacity 0.5s;
            z-index: 9999;
        `;

        document.body.appendChild(drop);
        cursorTrail.push(drop);

        setTimeout(() => {
            drop.style.opacity = '0';
            setTimeout(() => drop.remove(), 500);
        }, 100);
    });
}

// ===== Impact Calculator =====
function initImpactCalculator() {
    const calculator = document.getElementById('impactCalculator');
    if (!calculator) return;

    const donationsInput = calculator.querySelector('#donationsCount');
    const resultDiv = calculator.querySelector('#impactResult');

    donationsInput.addEventListener('input', (e) => {
        const donations = parseInt(e.target.value) || 0;
        const livesSaved = donations * 3;
        const unitsBlood = donations * 450; // ml

        resultDiv.innerHTML = `
            <div class="impact-stats">
                <div class="stat bounce-in">
                    <i class="fas fa-heartbeat"></i>
                    <h3>${livesSaved}</h3>
                    <p>Lives Saved</p>
                </div>
                <div class="stat bounce-in" style="animation-delay: 0.1s">
                    <i class="fas fa-tint"></i>
                    <h3>${(unitsBlood / 1000).toFixed(1)}L</h3>
                    <p>Blood Donated</p>
                </div>
            </div>
        `;
    });
}

// ===== Initialize All Features =====
function initAdvancedFeatures() {
    // Particle system
    const canvas = document.getElementById('particleCanvas');
    if (canvas) {
        const particles = new ParticleSystem(canvas);
        particles.start();
    }

    // Scroll reveal
    initScrollReveal();

    // Impact calculator
    initImpactCalculator();

    // Add ripple effect to buttons
    document.querySelectorAll('.btn, button').forEach(btn => {
        if (!btn.classList.contains('ripple-container')) {
            btn.classList.add('ripple-container');
            btn.addEventListener('click', createRipple);
        }
    });

    // Animate counters on scroll
    const counters = document.querySelectorAll('[data-counter]');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.dataset.counter);
                animateCounter(entry.target, target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => counterObserver.observe(counter));

    // Progress circles
    document.querySelectorAll('.progress-circle').forEach(circle => {
        const progressBar = circle.querySelector('.progress-bar');
        const percentage = parseInt(circle.dataset.progress || 0);
        if (progressBar) {
            updateProgressCircle(progressBar, percentage);
        }
    });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAdvancedFeatures);
} else {
    initAdvancedFeatures();
}
