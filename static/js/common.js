document.addEventListener('DOMContentLoaded', function() {
    // Select all flash messages
    const flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(function(message) {
        // Set a timeout to add the 'fade-out' class and remove the element
        setTimeout(function() {
            message.classList.add('fade-out');
            // Remove the element after the fade-out transition
            setTimeout(function() {
                message.remove();
            }, 1000); // Match the duration of your fade-out transition
        }, 3000); // Time before starting the fade-out effect
    });
});
