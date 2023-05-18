function addItem() {
    // Get values entered in form
    const name = document.querySelector('input[name="ProductBrand"]').value;
    const dateAdded = document.querySelector('input[name="dateAdded"]').value;
    const dateExpire = document.querySelector('input[name="dateExpire"]').value;
    const listSelect = document.querySelector('select[name="list-select"]').value;
  
    // Get the existing list of items for the selected list
    const items = JSON.parse(localStorage.getItem(listSelect)) || [];
  
    // Add the new item to the list
    items.push({ name, dateAdded, dateExpire });
  
    // Save the updated list to localStorage
    localStorage.setItem(listSelect, JSON.stringify(items));
  
    // Redirect to HomeScreen.html
    window.location.href = './HomeScreen.html';
  }
