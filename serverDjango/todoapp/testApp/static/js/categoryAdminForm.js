const categoryModal = document.querySelector(".category-modal");
const createCategoryBtn = document.querySelector(".category-create-btn");
const categoryCreateCancelBtn = document.querySelector(
  ".category-create-cancel"
);
const editCategoryBtns = document.querySelectorAll(".edit-category");
const categoryForm = document.querySelector(".category-form");
// const backdrop = document.querySelector(".backdrop");

createCategoryBtn.addEventListener("click", () => {
  categoryModal.classList.remove("hidden");
  backdrop.classList.remove("hidden");
});

categoryCreateCancelBtn.addEventListener("click", (e) => {
  e.preventDefault();
  categoryModal.classList.add("hidden");
  backdrop.classList.add("hidden");
});

editCategoryBtns.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    const categoryId = btn.getAttribute("data-category-id");
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
