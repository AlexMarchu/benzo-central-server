document.addEventListener('DOMContentLoaded', function() {
    document.documentElement.setAttribute('data-theme', 'light');
    document.body.setAttribute('data-theme', 'light');
    console.log('sldflsfsfs')
    
    const themeToggle = document.querySelector('button.theme-toggle');
    if (themeToggle) {
        themeToggle.remove();
    }
});