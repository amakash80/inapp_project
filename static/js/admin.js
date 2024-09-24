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


// Function to show the Edit User Modal with pre-filled user information
function showEditModal(uid, uname, uemail, uphone, ustate, ucity) {
    // Populate the form fields in the modal with the selected user's data
    document.getElementById('editUserId').value = uid;
    document.getElementById('editUserName').value = uname;
    document.getElementById('editUserEmail').value = uemail;
    document.getElementById('editUserPhoneNumber').value = uphone;
    document.getElementById('editUserState').value = ustate;
    document.getElementById('editUserCity').value = ucity;
    // Display the modal
    document.getElementById('editUserModal').style.display = 'block';
}

//Add User modal
function showAddUserModal() {
    document.getElementById('addUserModal').style.display = 'block';
}
//Confirm user delete
function userConfirmDelete() {
    return confirm("Are you sure you want to delete this user?");
}
function courseConfirmDelete() {
    return confirm("Are you sure you want to delete this course?");
}
//Add course modal
function openAddCourseModal() {
    document.getElementById('addCourseModal').style.display = 'block';
}

// Function to close the modal
function closeEditModal() {
    document.getElementById('editUserModal').style.display = 'none';
}
function closeAddUserModal() {
    document.getElementById('addUserModal').style.display = 'none';
}
function closeAddCourseModal() {
    document.getElementById('addCourseModal').style.display = 'none';
}

// Optional: You can add an event listener to close the modal when clicking outside of it
window.onclick = function(event) {
    var modal = document.getElementById('editUserModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Optional: Function to reset the form fields when the modal is closed or reopened
function resetEditForm() {
    document.getElementById('editUserForm').reset();
}

function showAddCourseModal() {
    document.getElementById('addCourseModal').style.display = 'block';
}

function closeAddCourseModal() {
    document.getElementById('addCourseModal').style.display = 'none';
}

function showEditCourseModal(cid, cname, cdescription, cduration, cfees) {
    document.getElementById('editCourseId').value = cid;
    document.getElementById('editCourseName').value = cname;
    document.getElementById('editCourseDescription').value = cdescription;
    document.getElementById('editCourseDuration').value = cduration;
    document.getElementById('editCourseFees').value = cfees;
    document.getElementById('editCourseModal').style.display = 'block';
}

function closeEditCourseModal() {
    document.getElementById('editCourseModal').style.display = 'none';
}

// function openEditCourseModal(course) {
//     // Populate the form fields with the current course data
//     document.getElementById('editCourseId').value = course.cid;
//     document.getElementById('editCourseName').value = course.cname;
//     document.getElementById('editCourseDescription').value = course.cdescription;
//     document.getElementById('editCourseDuration').value = course.cduration;
//     document.getElementById('editCourseFees').value = course.cfees;

//     // Open the modal
//     document.getElementById('editCourseModal').style.display = 'block';
// }

// function closeEditCourseModal() {
//     document.getElementById('editCourseModal').style.display = 'none';
// }

function openStatusModal(enquiryId) {
    document.getElementById('enquiry_id').value = enquiryId;
    document.getElementById('statusUpdateModal').style.display = 'block';
}

function closeStatusModal() {
    document.getElementById('statusUpdateModal').style.display = 'none';
}

