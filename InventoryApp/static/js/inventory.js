document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-button');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            document.getElementById('editItemId').value = this.dataset.id;
            document.getElementById('edit_name').value = this.dataset.name;
            document.getElementById('edit_status').value = this.dataset.status;
            document.getElementById('edit_category').value = this.dataset.category;
            document.getElementById('edit_sub_category').value = this.dataset.sub_category;
            document.getElementById('edit_brand').value = this.dataset.brand;
            document.getElementById('edit_model').value = this.dataset.model;
            document.getElementById('edit_color').value = this.dataset.color;
            document.getElementById('edit_value').value = this.dataset.value;
            document.getElementById('edit_location').value = this.dataset.location;
            document.getElementById('edit_last_maintained').value = this.dataset.last_maintained;

            const reorderCheckbox = document.getElementById('edit_reorder');
            reorderCheckbox.checked = this.dataset.reorder === 'True' || this.dataset.reorder === 'true';
        });
    });
});