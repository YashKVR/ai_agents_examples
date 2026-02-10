document.getElementById("add-todo").addEventListener("click", function() {
  const newTodoText = document.getElementById("new-todo").value;
  if (newTodoText) {
    const todoList = document.getElementById("todo-list");
    const listItem = document.createElement("li");
    listItem.textContent = newTodoText;
    listItem.addEventListener("click", function() {
      this.remove();
    });
    todoList.appendChild(listItem);
    document.getElementById("new-todo").value = "";
  }
});
