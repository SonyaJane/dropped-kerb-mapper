export default function resetForm() {
    // Clear the comments input value
    const commentsInput = document.getElementById('id_comments');
    commentsInput.value = "";
    
    // clear the photo input value
    document.getElementById('id_photo').value = "";

    // set the condition to green
    const conditionSelect = document.getElementById('condition');
    conditionSelect.value = "green";

    // clear any inline error next to condition
    const existingError = document.querySelector('.text-danger.inline-error');
    if (existingError) existingError.remove();

}