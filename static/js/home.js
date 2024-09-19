document.addEventListener("DOMContentLoaded", function() {
    // JavaScript for banner image rotation
    console.log("JS loaded");
    const images = document.querySelectorAll('.banner img');
    let currentIndex = 0;

    function showImage(index) {
        images[currentIndex].classList.remove('active');
        currentIndex = index;
        if (currentIndex < 0) currentIndex = images.length - 1;
        if (currentIndex >= images.length) currentIndex = 0;
        images[currentIndex].classList.add('active');
    }

    document.querySelector('.banner .left').addEventListener('click', () => {
        showImage(currentIndex - 1);
    });

    document.querySelector('.banner .right').addEventListener('click', () => {
        showImage(currentIndex + 1);
    });

    setInterval(() => {
        showImage(currentIndex + 1);
    }, 5000); // Auto-rotate every 5 seconds

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
