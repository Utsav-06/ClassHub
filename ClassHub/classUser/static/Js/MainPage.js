// Redirect to page code

function redirectToPage(arrowId) {
  switch (arrowId) {
    case 'task-arrow':
      window.location.href = "{% url 'list_task' %}"
      break
    case 'assignment-arrow':
      window.location.href = "{% url 'list_assignment' %}"
      break
    case 'material-arrow':
      window.location.href = "{% url 'list_materials' %}"
      break
    case 'reminder-arrow':
      window.location.href = "{% url 'list_reminder' %}"
      break
    case 'expense-arrow':
      window.location.href = "{% url 'list_expense' %}"
      break

    case 'task-add':
      window.location.href = "{% url 'add_task' %}"
      break
    case 'assignment-add':
      window.location.href = "{% url 'add_assignment' %}"
      break
    case 'material-add':
      window.location.href = "{% url 'add_material' %}"
      break
    case 'reminder-add':
      window.location.href = "{% url 'set_reminder' %}"
      break
    case 'expense-add':
      window.location.href = "{% url 'add_expense' %}"
      break

    case 'main-page':
      window.location.href = "{% url 'main' %}"
      break
  }
}

// Code for saving the last user theme preference along with theme toggling logic

document.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    document.body.setAttribute('theme', savedTheme)
    document.getElementById('theme-toggle').checked = savedTheme === 'dark'
    const label = document.querySelector('#theme-toggle + label')
    label.classList.toggle('dark-mode', savedTheme === 'dark')
  }
})

document.getElementById('theme-toggle').addEventListener('click', (e) => {
  const checked = e.target.checked
  document.body.setAttribute('theme', checked ? 'dark' : 'light')
  localStorage.setItem('theme', checked ? 'dark' : 'light')
  const label = document.querySelector('#theme-toggle + label')
  label.classList.toggle('dark-mode', checked)
})

function submitForm() {
  console.log(document.getElementById('theme-toggle').checked)
  document.getElementById('theme-form').submit()
}
