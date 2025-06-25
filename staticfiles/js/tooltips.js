export default function showTooltip(btnId, tooltipId) {
    // This function is used to show the tooltip for the satellite toggle button
    // when the user hovers over it or touches and holds it on mobile devices.
    const btn = document.getElementById(btnId);
    let hoverTimer, touchTimer;
    let tooltipActive = false;

    function showTooltipClass() {
        if (tooltipActive) btn.classList.add('show-tooltip');
    }

    function clearAll() {
        clearTimeout(hoverTimer);
        clearTimeout(touchTimer);
        tooltipActive = false;
        btn.classList.remove('show-tooltip');
    }

    btn.addEventListener('mouseenter', () => {
        tooltipActive = true;
        hoverTimer = setTimeout(showTooltipClass, 1000);
    });

    // Mouse leaves/clicks/etc
    btn.addEventListener('mouseleave', clearAll);
    btn.addEventListener('mousedown', clearAll);
    btn.addEventListener('mouseup', clearAll);
    btn.addEventListener('click', clearAll);

    // Touch (mobile)
    btn.addEventListener('touchstart', () => {
        tooltipActive = true;
        touchTimer = setTimeout(showTooltipClass, 1000);
    });
    btn.addEventListener('touchend', clearAll);
    btn.addEventListener('touchcancel', clearAll);
};
