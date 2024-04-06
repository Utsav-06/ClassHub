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