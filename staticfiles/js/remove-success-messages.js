// This script will remove messages after 5 seconds
function removeMessages() {
    document.querySelectorAll('.alert').forEach(el => {
      // fade out
      el.style.transition = 'opacity 0.5s';
      el.style.opacity = '0';
      // remove after fade
      setTimeout(() => el.remove(), 500);
    });
  }
  
// run on initial page load
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(removeMessages, 5000);
});

// run after any HTMX swap into #message-container
document.body.addEventListener('htmx:afterSwap', e => {
    console.log('htmx:afterSwap', e.detail.target.id);
    if (e.detail.target.id === 'new-report-container') {
        setTimeout(removeMessages, 5000);
    }
});