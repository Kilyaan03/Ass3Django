// Get references to the menu button, menu bar, and menu item elements
let menuButton = document.getElementById("menuButton");
let menuBar = document.getElementById("menuBar");
let menuItem = document.getElementById("menu-item");

// Add an event listener to the menu button to show the menu bar on mouseover
menuButton.addEventListener("mouseover", event => {
    menuBar.classList.add("view"); //adds class view to menubar
});

// Add an event listener to the menu bar to hide the menu bar on mouseleave
menuBar.addEventListener("mouseleave", event => {
    menuBar.classList.remove("view");//when mouse leaves menu bar it removese view therefore making i tinvisible again
    resetMenuBar(); // use the function resetMenuBar to reset the menu bar state
});

// Add an event listener to the document to run code when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get all elements with the class 'menu-header'
    const headers = document.querySelectorAll('.menu-header');
    // Get all elements with the class 'menu-item'
    const menuItems = document.querySelectorAll('.menu-item');
    
    // Add a click event listener to each menu header
    headers.forEach(header => {
        header.addEventListener('click', function() {
            // Get the target element ID from the data-target attribute
            const targetId = this.getAttribute('data-target');
            // Get the target element by ID
            const targetElement = document.getElementById(targetId);
            
            // If the target element exists, toggle its visibility
            if (targetElement) {
                targetElement.classList.toggle('visible');
            }
        });
    });

    // Add a click event listener to each menu item
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            // Get the URL from the data-url attribute
            const url = this.getAttribute('data-url');
            // Redirect to the URL
            window.location.href = url;
        });
    });
});

// Function to reset the menu bar state
function resetMenuBar() {
    // Get all elements with the class 'menu-options'
    const menuOptions = document.querySelectorAll('.menu-options');
    // Remove the 'visible' class from each menu option
    menuOptions.forEach(option => {
        option.classList.remove('visible');
    });
}