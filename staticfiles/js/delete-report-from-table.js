document.addEventListener('DOMContentLoaded', function () {
    const deleteModal = document.getElementById('delete-modal');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    console.log('Delete modal:', deleteModal);
    // Listen for all delete buttons
    document.querySelectorAll('.delete-report-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            console.log('Delete button clicked');
            const reportId = this.getAttribute('data-report-id');
            console.log(`Report ID to delete: ${reportId}`);
            console.log('href current', confirmDeleteBtn.href);
            // Set the href for the confirm button
            confirmDeleteBtn.href = `/reports/${reportId}/delete/`; // Adjust URL as needed
        });
    });
});