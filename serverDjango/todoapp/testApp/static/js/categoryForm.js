const categoryModal = document.querySelector(".category-modal");
const createCategoryBtn = document.querySelector(".category-create-btn");
const categoryCreateCancelBtn = document.querySelector(
  ".category-create-cancel"
);
const editCategoryBtns = document.querySelectorAll(".edit-category");
const deleteCategoryBtns = document.querySelectorAll(".delete-category");
const categoryForm = document.querySelector(".category-form");
const saveBtn = document.querySelector(".save");
const updateBtn = document.querySelector(".update");
const title = document.querySelector(".category-title");
let categoryId;
// const backdrop = document.querySelector(".backdrop");

createCategoryBtn.addEventListener("click", () => {
  categoryModal.classList.remove("hidden");
  backdrop.classList.remove("hidden");
});

categoryCreateCancelBtn.addEventListener("click", (e) => {
  e.preventDefault();
  title.innerHTML = "Create Category";
  categoryModal.classList.add("hidden");
  backdrop.classList.add("hidden");
  updateBtn.classList.add("hidden");
  saveBtn.classList.remove("hidden");
});

editCategoryBtns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();

    title.innerHTML = "Update Category";
    updateBtn.classList.remove("hidden");
    saveBtn.classList.add("hidden");

    categoryId = btn.getAttribute("data-category-id");
    fetch(`categories/${categoryId}/`)
      .then((response) => response.json())
      .then((data) => {
        populateCategoryForm(data);
        categoryModal.classList.remove("hidden");
        backdrop.classList.remove("hidden");
      })
      .catch((error) => console.error("Error fetching task data:", error));
  });
});

function populateCategoryForm(categoryData) {
  categoryForm.querySelector('input[name="categoryName"]').value =
    categoryData.name;
}

updateBtn.addEventListener("click", async (e) => {
  e.preventDefault();
  const data = {
    name: categoryForm.querySelector('input[name="categoryName"]').value,
  };

  const category = await fetch(
    `http://127.0.0.1:8000/categories/${categoryId}/`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json", // Specify the content type as JSON
      }, // Specify the HTTP method as PUT
      body: JSON.stringify(data), // Pass the form data in the body
    }
  );

  if (await category) {
    window.location.reload();
  }
});

deleteCategoryBtns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();

    categoryId = btn.getAttribute("data-category-id");
    fetch(`categories/${categoryId}/`, { method: "DELETE" })
      .then((response) => (window.location.href = window.location.href))
      .catch((error) => console.error("Error fetching task data:", error));
  });
});
