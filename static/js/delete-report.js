const deleteModal = new bootstrap.Modal(document.getElementById("delete-modal"));
const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
const deleteBtn = document.querySelector('.delete-report-btn');

deleteBtn.addEventListener("click", (e) => {
    // Reset button text and state
    confirmDeleteBtn.textContent = 'Delete';
    confirmDeleteBtn.classList.remove('disabled');
    const cancelBtn = document.getElementById('delete-modal').querySelector('.btn-secondary');
    if (cancelBtn) {
        cancelBtn.disabled = false;
    }
    // Add click handler to change text to 'Deleting'
    confirmDeleteBtn.onclick = function (e) {
        confirmDeleteBtn.textContent = 'Deleting...';
        confirmDeleteBtn.classList.add('disabled');
        if (cancelBtn) {
            cancelBtn.disabled = true;
        }
        // Prevent further clicks and navigation
        //e.preventDefault();
    };
});
