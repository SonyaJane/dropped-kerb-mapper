/** 
* Removes all messages after 5 seconds
*/
export default function removeAllMessages() {
  document.querySelectorAll('.alert').forEach(el => {
      // after 5 s, start fade
      setTimeout(() => {
      el.style.transition = 'opacity 0.5s';
      el.style.opacity = '0';
      // remove 0.5 s later
      setTimeout(() => el.remove(), 500);
    }, 5000);
  });
} 