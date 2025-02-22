// Store inventory URL from Django
const inventoryUrl = window.inventoryUrl || "/inventory/";  // Ensure fallback if Django template didn't pass it

function editItem(id, name, value, status, category, sub_category, brand, model, color, reorder, location, last_maintained) {
    document.getElementById('editInventoryForm').action = `/update_item/${id}/`;
    document.getElementById('editItemId').value = id;
    document.getElementById('edit_name').value = name;
    document.getElementById('edit_value').value = value;
    document.getElementById('edit_status').value = status;
    document.getElementById('edit_category').value = category;
    document.getElementById('edit_sub_category').value = sub_category;
    document.getElementById('edit_brand').value = brand;
    document.getElementById('edit_model').value = model;
    document.getElementById('edit_color').value = color;
    document.getElementById('edit_reorder').checked = reorder === true || reorder === 'true';
    document.getElementById('edit_location').value = location;
    document.getElementById('edit_last_maintained').value = last_maintained || ''; // Prevents null issues

    new bootstrap.Modal(document.getElementById('editItemModal')).show();
}

function confirmDeleteItem() {
    return confirm('Are you sure you want to delete this item?');
}

function deleteItem() {
    const id = document.getElementById('editItemId').value;
    if (confirmDeleteItem()) {
        const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        if (!csrfTokenElement) {
            alert('CSRF token not found!');
            return;
        }

        fetch(`/delete_item/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfTokenElement.value,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => {
                if (response.ok) {
                    const modalElement = document.getElementById('editItemModal');
                    const modalInstance = bootstrap.Modal.getInstance(modalElement);
                    if (modalInstance) modalInstance.hide();

                    window.location.href = inventoryUrl;
                } else {
                    alert('Failed to delete item');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error deleting item');
            });
    }
}

$(document).ready(function () {
    $('#inventoryTable').DataTable({ pageLength: 25 });

    $('#editInventoryForm').on('submit', function (e) {
        e.preventDefault();

        const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        if (!csrfTokenElement) {
            alert('CSRF token not found!');
            return;
        }

        fetch(this.action, {
            method: 'POST',
            body: new FormData(this),
            headers: {
                'X-CSRFToken': csrfTokenElement.value,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const modalElement = document.getElementById('editItemModal');
                    const modalInstance = bootstrap.Modal.getInstance(modalElement);
                    if (modalInstance) modalInstance.hide();

                    window.location.href = inventoryUrl;
                } else {
                    alert('Form submission failed. Check console for details.');
                    console.error('Form submission failed:', data.errors);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while submitting the form.');
            });
    });
});
