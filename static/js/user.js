document.addEventListener("DOMContentLoaded", function() {
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
    // Edit Profile Modal
    var editProfileModal = document.getElementById("editProfileModal");
    var editProfileBtn = document.getElementById("editProfileBtn");
    var editProfileClose = document.getElementsByClassName("close")[0];

    if (editProfileBtn) {
        editProfileBtn.onclick = function() {
            editProfileModal.style.display = "block";
        }
    }

    if (editProfileClose) {
        editProfileClose.onclick = function() {
            editProfileModal.style.display = "none";
        }
    }

    // Delete Profile Modal
    var deleteProfileModal = document.getElementById("deleteProfileModal");
    var deleteProfileBtn = document.getElementById("deleteProfileBtn");
    var deleteProfileClose = document.getElementsByClassName("close")[1];
    var cancelDeleteBtn = document.getElementsByClassName("cancel-delete")[0];
    var confirmDeleteBtn = document.getElementById("confirmDeleteBtn");

    if (deleteProfileBtn) {
        deleteProfileBtn.onclick = function() {
            deleteProfileModal.style.display = "block";
        }
    }

    if (deleteProfileClose) {
        deleteProfileClose.onclick = function() {
            deleteProfileModal.style.display = "none";
        }
    }

    if (cancelDeleteBtn) {
        cancelDeleteBtn.onclick = function() {
            deleteProfileModal.style.display = "none";
        }
    }

    if (confirmDeleteBtn) {
        confirmDeleteBtn.onclick = function() {
            deleteProfileModal.style.display = "none";
        }
    }

    // Toggle between profile, enquiries, and add enquiry sections
    var profileSection = document.getElementById("profile-section");
    var enquiriesSection = document.getElementById("enquiries-section");
    var addEnquirySection = document.getElementById("add-enquiry-section");
    var profileMenuItem = document.getElementById("profileMenuItem");
    var enquiriesMenuItem = document.getElementById("enquiriesMenuItem");
    var addEnquiryMenuItem = document.getElementById("addEnquiryMenuItem");

    if (profileMenuItem) {
        profileMenuItem.addEventListener("click", function() {
            profileSection.style.display = "block";
            enquiriesSection.style.display = "none";
            addEnquirySection.style.display = "none";
            profileMenuItem.classList.add("active");
            enquiriesMenuItem.classList.remove("active");
            addEnquiryMenuItem.classList.remove("active");
        });
    }

    if (enquiriesMenuItem) {
        enquiriesMenuItem.addEventListener("click", function() {
            profileSection.style.display = "none";
            enquiriesSection.style.display = "block";
            addEnquirySection.style.display = "none";
            profileMenuItem.classList.remove("active");
            enquiriesMenuItem.classList.add("active");
            addEnquiryMenuItem.classList.remove("active");
        });
    }

    if (addEnquiryMenuItem) {
        addEnquiryMenuItem.addEventListener("click", function() {
            profileSection.style.display = "none";
            enquiriesSection.style.display = "none";
            addEnquirySection.style.display = "block";
            profileMenuItem.classList.remove("active");
            enquiriesMenuItem.classList.remove("active");
            addEnquiryMenuItem.classList.add("active");
        });
    }

    // Clear form button
    var clearFormBtn = document.getElementById("clearFormBtn");
    if (clearFormBtn) {
        clearFormBtn.addEventListener("click", function() {
            document.getElementById("addEnquiryForm").reset();
        });
    }

    // Close modals if clicking outside of them
    window.onclick = function(event) {
        if (event.target == editProfileModal) {
            editProfileModal.style.display = "none";
        }
        if (event.target == deleteProfileModal) {
            deleteProfileModal.style.display = "none";
        }
        if (event.target == document.getElementById("allEnquiriesModal")) {
            closeModal();
        }
    }

    // Open modal
    function openModal() {
        document.getElementById("allEnquiriesModal").style.display = "block";
    }

    // Close modal
    function closeModal() {
        document.getElementById("allEnquiriesModal").style.display = "none";
    }

});

