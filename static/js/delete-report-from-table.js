document.addEventListener('DOMContentLoaded', function () {
    const deleteModal = document.getElementById('delete-modal');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    // Listen for all delete buttons
    document.querySelectorAll('.delete-report-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const reportId = this.getAttribute('data-report-id');
            // Set the href for the confirm button
            confirmDeleteBtn.href = `/reports/${reportId}/delete/`;
            // Reset button text in case it was changed previously
            confirmDeleteBtn.textContent = 'Delete';
            // Find the cancel button in the modal
            const cancelBtn = deleteModal.querySelector('.btn-secondary');
            if (cancelBtn) {
                cancelBtn.disabled = false;
            }
            // Add click handler to change text to 'Deleting'
            confirmDeleteBtn.onclick = function () {
                confirmDeleteBtn.textContent = 'Deleting...';
                confirmDeleteBtn.classList.add('disabled');
                if (cancelBtn) {
                    cancelBtn.disabled = true;
                }
                // Prevent further clicks and navigation
                e.preventDefault();
            };
        });
    });
});