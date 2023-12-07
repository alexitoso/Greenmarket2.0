// static/js/custom.js
window.onload = function() {
    if (window.history && window.history.pushState) {
        window.history.pushState('forward', null, './#forward');
        window.onpopstate = function(event) {
            window.history.pushState('forward', null, './#forward');
        };
    }
};