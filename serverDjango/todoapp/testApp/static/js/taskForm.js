const taskModal = document.querySelector(".task-modal");
const createTaskBtn = document.querySelector(".task-create-btn");
const taskCreateCancelBtn = document.querySelector(".task-create-cancel");
const taskForm = document.querySelector(".task-form");
const editTaskBtns = document.querySelectorAll(".edit-task");
const deleteTaskBtns = document.querySelectorAll(".delete-task");
const saveBtn = document.querySelector(".save");
const updateBtn = document.querySelector(".update");
const title = document.querySelector(".task-title");
let taskId;
createTaskBtn.addEventListener("click", () => {
  title.innerHTML = "Create Task";
  taskModal.classList.remove("hidden");
  backdrop.classList.remove("hidden");
  updateBtn.classList.add("hidden");
  saveBtn.classList.remove("hidden");
});

taskCreateCancelBtn.addEventListener("click", (e) => {
  e.preventDefault();
  taskModal.classList.add("hidden");
  backdrop.classList.add("hidden");
  updateBtn.classList.add("hidden");
  saveBtn.classList.remove("hidden");
  title.innerHTML = "Create Task";
});

editTaskBtns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    title.innerHTML = "Update Task";
    updateBtn.classList.remove("hidden");
    saveBtn.classList.add("hidden");

    taskId = btn.getAttribute("data-task-id");
    fetch(`tasks/${taskId}/`)
      .then((response) => response.json())
      .then((data) => {
        populateTaskForm(data);
        taskModal.classList.remove("hidden");
        backdrop.classList.remove("hidden");
      })
      .catch((error) => console.error("Error fetching task data:", error));
  });
});

function populateTaskForm(taskData) {
  taskForm.querySelector('input[name="title"]').value = taskData.title;
  taskForm.querySelector('textarea[name="description"]').value =
    taskData.description;
  taskForm.querySelector('input[name="deadline"]').value = taskData.deadline;
  const capitalizedStatus =
    taskData.status.charAt(0).toUpperCase() + taskData.status.slice(1);
  taskForm.querySelector('select[name="status"]').value = capitalizedStatus;

  const categoriesSelect = taskForm.querySelector('select[name="category"]');
  const categoryId = taskData.category.id;
  const options = categoriesSelect.options;

  for (let i = 0; i < options.length; i++) {
    if (options[i].value == categoryId) {
      options[i].selected = true;
      break;
    }
  }
}

updateBtn.addEventListener("click", async (e) => {
  e.preventDefault();

  const data = {
    title: taskForm.querySelector('input[name="title"]').value,
    description: taskForm.querySelector('textarea[name="description"]').value,
    deadline: taskForm.querySelector('input[name="deadline"]').value,
    status: taskForm.querySelector('select[name="status"]').value,
    category_id: taskForm.querySelector('select[name="category"]').value,
  };

  const task = await fetch(`http://127.0.0.1:8000/tasks/${taskId}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json", // Specify the content type as JSON
    }, // Specify the HTTP method as PUT
    body: JSON.stringify(data), // Pass the form data in the body
  });

  if (await task) {
    window.location.reload();
  }
});

deleteTaskBtns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();

    taskId = btn.getAttribute("data-task-id");
    fetch(`tasks/${taskId}/`, { method: "DELETE" })
      .then((response) => (window.location.href = window.location.href))
      .catch((error) => console.error("Error fetching task data:", error));
  });
});
