// Redirect to page code

function redirectToPage(arrowId) {
  switch (arrowId) {
    case 'task-arrow':
      window.location.href = urls.listTask;
      break;
    case 'assignment-arrow':
      window.location.href = urls.listAssignment;
      break;
    case 'material-arrow':
      window.location.href = urls.listMaterials;
      break;
    case 'reminder-arrow':
      window.location.href = urls.listReminder;
      break;
    case 'expense-arrow':
      window.location.href = urls.listExpense;
      break;

    case 'task-add':
      window.location.href = urls.addTask;
      break;
    case 'assignment-add':
      window.location.href = urls.addAssignment;
      break;
    case 'material-add':
      window.location.href = urls.addMaterial;
      break;
    case 'reminder-add':
      window.location.href = urls.setReminder;
      break;
    case 'expense-add':
      window.location.href = urls.addExpense;
      break;

    case 'main-page':
      window.location.href = urls.mainPage;
      break;
  }
}

// Code for saving the last user theme preference along with theme toggling logic

document.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    document.body.setAttribute('theme', savedTheme);
    document.getElementById('theme-toggle').checked = savedTheme === 'dark';
    const label = document.querySelector('#theme-toggle + label');
    label.classList.toggle('dark-mode', savedTheme === 'dark');
  }
});

document.getElementById('theme-toggle').addEventListener('click', (e) => {
  const checked = e.target.checked;
  document.body.setAttribute('theme', checked ? 'dark' : 'light');
  localStorage.setItem('theme', checked ? 'dark' : 'light');
  const label = document.querySelector('#theme-toggle + label');
  label.classList.toggle('dark-mode', checked);
});

function sessionThemeManagement() {
  const themeToggle = document.getElementById("theme-toggle");
  if (themeToggle.checked) {
    sessionStorage.setItem("theme", "dark");
  } else {
    sessionStorage.setItem("theme", "light");
  }
}

