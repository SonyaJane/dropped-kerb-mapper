// Add an event listener to the form submission
document.addEventListener('DOMContentLoaded', function () {
    // Add an event listener to the form submission
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function () {
            // Disable the submit button
            const submitButton = document.getElementById('submit-button');
            submitButton.disabled = true;
            submitButton.textContent = 'Sending...'; // Change button text to indicate progress

            // Show the loading message
            document.getElementById('loading-message').style.display = 'block';
        });
    }
});