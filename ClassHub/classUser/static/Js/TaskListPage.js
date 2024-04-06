//  Modal
let TaskModal = document.getElementById('TaskModal')
let overlay = document.getElementById('overlay')

function openAddTaskModal() {
    TaskModal.classList.add('open-TaskModal')
    overlay.classList.add('open-overlay')
}

function closeAddTaskModal() {
    TaskModal.classList.remove('open-TaskModal')
    overlay.classList.remove('open-overlay')
}


// Theme

document.addEventListener("DOMContentLoaded", function () {
    const theme = sessionStorage.getItem("theme");
    if (theme === "dark") {
        document.body.classList.add("dark-theme");
    } else {
        document.body.classList.remove("dark-theme");
    }
});