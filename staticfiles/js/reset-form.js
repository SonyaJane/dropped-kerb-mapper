export default function resetForm() {
    // Clear the comments input value
    const commentsInput = document.getElementById('id_comments');
    commentsInput.value = "";
    
    // clear the photo input value
    document.getElementById('id_photo').value = "";

    // set the condition to green
    const conditionSelect = document.getElementById('condition');
    conditionSelect.value = "green";
}