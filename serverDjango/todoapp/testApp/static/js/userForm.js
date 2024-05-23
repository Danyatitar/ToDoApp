const userModal = document.querySelector(".user-modal");
const createUserBtn = document.querySelector(".user-create-btn");
const userCreateCancelBtn = document.querySelector(".user-create-cancel");
const userForm = document.querySelector(".user-form");
const editUserBtns = document.querySelectorAll(".edit-user");
const deleteUserBtns = document.querySelectorAll(".delete-user");
const saveBtn = document.querySelector(".save");
const updateBtn = document.querySelector(".update");
const title = document.querySelector(".user-title");
let userId;

createUserBtn.addEventListener("click", () => {
  title.innerHTML = "Create User";
  userModal.classList.remove("hidden");
  backdrop.classList.remove("hidden");
  updateBtn.classList.add("hidden");
  saveBtn.classList.remove("hidden");
});

userCreateCancelBtn.addEventListener("click", (e) => {
  e.preventDefault();
  userModal.classList.add("hidden");
  backdrop.classList.add("hidden");
});

editUserBtns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();

    title.innerHTML = "Update User";
    updateBtn.classList.remove("hidden");
    saveBtn.classList.add("hidden");

    userId = btn.getAttribute("data-user-id");
    fetch(`users/${userId}/`)
      .then((response) => response.json())
      .then((data) => {
        populateUserForm(data);
        userModal.classList.remove("hidden");
        backdrop.classList.remove("hidden");
      })
      .catch((error) => console.error("Error fetching task data:", error));
  });
});
function populateUserForm(userData) {
  userForm.querySelector('input[name="username"]').value = userData.name;
  userForm.querySelector('input[name="email"]').value = userData.email;
  const capitalizedStatus =
    userData.role.charAt(0).toUpperCase() + userData.role.slice(1);
  userForm.querySelector('select[name="role"]').value = capitalizedStatus;
}

updateBtn.addEventListener("click", async (e) => {
  e.preventDefault();

  const data = {
    name: userForm.querySelector('input[name="username"]').value,
    email: userForm.querySelector('input[name="email"]').value,
    role: userForm.querySelector('select[name="role"]').value,
  };

  const user = await fetch(
    `http://127.0.0.1:8000/administrator/users/${userId}/`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json", // Specify the content type as JSON
      }, // Specify the HTTP method as PUT
      body: JSON.stringify(data), // Pass the form data in the body
    }
  );

  if (await user) {
    window.location.reload();
  }
});

deleteUserBtns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();

    userId = btn.getAttribute("data-user-id");
    fetch(`users/${userId}/`, { method: "DELETE" })
      .then((response) => (window.location.href = window.location.href))
      .catch((error) => console.error("Error fetching user data:", error));
  });
});
