const changeNameModal = document.querySelector(".change-name-modal");
const changeNameBtn = document.querySelector(".changeName");
const changeNameCancelBtn = document.querySelector(".changeName-cancel");
const backdrop = document.querySelector(".backdrop");

changeNameBtn.addEventListener("click", () => {
  changeNameModal.classList.remove("hidden");
  backdrop.classList.remove("hidden");
});

changeNameCancelBtn.addEventListener("click", (e) => {
  e.preventDefault();
  changeNameModal.classList.add("hidden");
  backdrop.classList.add("hidden");
});
