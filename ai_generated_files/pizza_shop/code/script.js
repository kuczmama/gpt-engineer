document.addEventListener("DOMContentLoaded", function() {
    renderMenuItems();
});

function renderMenuItems() {
    var menuItems = ["Margherita", "Pepperoni", "Hawaiian", "Veggie"];

    var menuList = document.getElementById("menu-list");
    for (var i = 0; i < menuItems.length; i++) {
        var menuItem = document.createElement("li");
        menuItem.textContent = menuItems[i];
        menuItem.addEventListener("click", toggleActiveClass); // Added to add click event to each menu item
        menuList.appendChild(menuItem);
    }
}

function toggleActiveClass(event) {
    var clickedItem = event.target;
    clickedItem.classList.toggle("active");
}