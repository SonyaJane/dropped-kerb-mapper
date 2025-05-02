// This script will remove success messages after 5 seconds
setTimeout(function(){
    document.querySelectorAll('.alert-success').forEach(function(el){
        // fade out
        el.style.transition = 'opacity 0.5s';
        el.style.opacity = '0';
        // remove after fade
        setTimeout(function(){ el.remove(); }, 500);
    });
}, 5000);