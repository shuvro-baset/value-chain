console.log("I am here............")
//
// function addRow() {
//   event.preventDefault()
//   var table = document.getElementById("myTable");
//   var row = table.insertRow(-1);
//   var rowCount = table.rows.length;
//
//   for (var i = 0; i < 4; i++) {
//     var cell = row.insertCell(-1);
//     var input = document.createElement("input");
//
//     if (i === 0) {
//       input = document.createElement("select");
//       input.name = "select1_" + rowCount;
//       // Populate select with options (excluding selected products)
//       populateSelect(input, rowCount);
//     } else {
//       input.type = "text";
//       input.name = "input" + (i + 1) + "_" + rowCount;
//     }
//
//     cell.appendChild(input);
//   }
// }
//
// function populateSelect(select, rowCount) {
//   // Fetch available products from Django backend (excluding selected ones)
//   fetchAvailableProducts(rowCount).then(products => {
//     products.forEach(product => {
//       var option = document.createElement("option");
//       option.value = product.id;
//       option.text = product.name;
//       select.appendChild(option);
//     });
//   });
// }
//
// function fetchAvailableProducts(rowCount) {
//   // Replace with your AJAX logic to fetch available products from Django
//   return fetch("/fetch-available-products/?selected_products=" + getSelectedProducts(rowCount))
//     .then(response => response.json());
// }
//
// function getSelectedProducts(rowCount) {
//   // Get IDs of selected products in previous rows
//   var selectedIds = [];
//   for (var i = 0; i < rowCount; i++) {
//     var selectedProductId = document.querySelector("#myTable select[name='select1_" + i + "']").value;
//     if (selectedProductId) {
//       selectedIds.push(selectedProductId);
//     }
//   }
//   return selectedIds.join(",");
// }


var usedProducts = [];

function addRow() {
    event.preventDefault()
    var table = document.getElementById("myTable");
    var rowCount = table.rows.length;
    var row = table.insertRow(-1);

    for (var i = 0; i < 4; i++) {
        var cell = row.insertCell(-1);
        var input = document.createElement("input");

        if (i === 0) {
            input = document.createElement("select");
            input.name = "product_" + rowCount;
            populateSelect(input, rowCount);
        } else {
            input.type = (i === 2) ? "number" : "text";  // Number input for qty
            input.step = "0.01";  // For decimal precision in qty
            input.name = "input" + (i + 1) + "_" + rowCount;
        }

        cell.appendChild(input);
    }
}

function populateSelect(select, rowCount) {
    fetchAvailableProducts(rowCount).then(products => {
        products.forEach(product => {
            var option = document.createElement("option");
            option.value = product.id;
            option.text = product.name;
            select.appendChild(option);
        });
    });
}

function fetchAvailableProducts(rowCount) {
    return fetch("/fetch-available-products/?selected_products=" + getSelectedProducts(rowCount))
        .then(response => response.json());
}

function getSelectedProducts(rowCount) {
    var selectedIds = [];
    for (var i = 0; i < rowCount; i++) {
        var selectedProductId = document.querySelector("#myTable select[name='product_" + i + "']").value;
        if (selectedProductId) {
            selectedIds.push(selectedProductId);
        }
    }
    return selectedIds.join(",");
}

function removeRow(button) {
    var row = button.parentNode.parentNode;
    var table = row.parentNode;
    table.deleteRow(row.rowIndex);
}