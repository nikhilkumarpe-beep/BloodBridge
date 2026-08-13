
// ===== Testimonials Carousel =====
function initTestimonials() {
    let slideIndex = 0;
    const slides = document.getElementsByClassName("testimonial-slide");

    if (slides.length === 0) return;

    function showSlides() {
        for (let i = 0; i < slides.length; i++) {
            slides[i].classList.remove("active");
        }
        slideIndex++;
        if (slideIndex > slides.length) { slideIndex = 1 }
        slides[slideIndex - 1].classList.add("active");
        setTimeout(showSlides, 5000); // Change slide every 5 seconds
    }

    showSlides();
}

// ===== Eligibility Quiz =====
function initQuiz() {
    const quizBtn = document.getElementById('startQuizBtn');
    const modal = document.getElementById('quizModal');
    const closeBtn = document.querySelector('.close-modal');
    const submitQuiz = document.getElementById('submitQuiz');

    if (!quizBtn || !modal) return;

    quizBtn.onclick = function () {
        modal.style.display = "block";
    }

    if (closeBtn) {
        closeBtn.onclick = function () {
            modal.style.display = "none";
        }
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Handle Quiz Selection
    const options = document.querySelectorAll('.quiz-option');
    options.forEach(option => {
        option.addEventListener('click', function () {
            // Toggle selection
            const radio = this.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
            }
        });
    });

    if (submitQuiz) {
        submitQuiz.onclick = function () {
            const age = document.querySelector('input[name="age"]:checked');
            const weight = document.querySelector('input[name="weight"]:checked');
            const health = document.querySelector('input[name="health"]:checked');

            const resultDiv = document.getElementById('quizResult');

            if (age && weight && health) {
                if (age.value === 'yes' && weight.value === 'yes' && health.value === 'yes') {
                    resultDiv.innerHTML = '<div style="padding: 15px; background: #d4edda; color: #155724; border-radius: 8px; margin-bottom: 20px;"><i class="fas fa-check-circle"></i> Great! You are likely eligible to donate blood. <a href="/signup" style="color: #155724; font-weight: bold;">Register Now</a></div>';
                } else {
                    resultDiv.innerHTML = '<div style="padding: 15px; background: #fff3cd; color: #856404; border-radius: 8px; margin-bottom: 20px;"><i class="fas fa-exclamation-circle"></i> You may not be eligible at this time. Please consult a doctor.</div>';
                }
            } else {
                resultDiv.innerHTML = '<div style="padding: 15px; background: #f8d7da; color: #721c24; border-radius: 8px; margin-bottom: 20px;">Please answer all questions.</div>';
            }
        }
    }
}
