
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
        setTimeout(showSlides, 5000); // Change image every 5 seconds
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
            if (this.classList.contains('selected')) {
                this.classList.remove('selected');
            } else {
                this.classList.add('selected');
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
                    resultDiv.innerHTML = '<div class="alert alert-success"><i class="fas fa-check-circle"></i> Great! You are likely eligible to donate blood. <a href="/signup">Register Now</a></div>';
                } else {
                    resultDiv.innerHTML = '<div class="alert alert-warning"><i class="fas fa-exclamation-circle"></i> You may not be eligible at this time. Please consult a doctor.</div>';
                }
            } else {
                resultDiv.innerHTML = '<div class="alert alert-danger">Please answer all questions.</div>';
            }
        }
    }
}
