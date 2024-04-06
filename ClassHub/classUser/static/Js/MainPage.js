// Redirect to page code

function redirectToPage(page) {
  const urls = {
    'main-page': '{% url "main" %}',
    'task-arrow': '{% url "list_task" %}',
    'assignment-arrow': '{% url "list_assignment" %}',
    'material-arrow': '{% url "list_materials" %}',
    'reminder-arrow': '{% url "list_reminder" %}',
    'expense-arrow': '{% url "list_expense" %}',
    'task-add': '{% url "add_task" %}',
    'assignment-add': '{% url "add_assignment" %}',
    'material-add': '{% url "add_material" %}',
    'reminder-add': '{% url "set_reminder" %}',
    'expense-add': '{% url "add_expense" %}'
  };
  window.location.href = urls[page];
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
