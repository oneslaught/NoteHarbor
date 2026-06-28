function toggleMenu() {
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.getElementById('hamburger');
    sidebar.classList.toggle('open');
    hamburger.classList.toggle('active');
}

document.addEventListener('click', function(e) {
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.getElementById('hamburger');
    if (!sidebar.contains(e.target)) {
        sidebar.classList.remove('open');
        hamburger.classList.remove('active');
    }
});