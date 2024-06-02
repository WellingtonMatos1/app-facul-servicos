document.getElementById('productImage').addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function() {
            const imagePreview = document.querySelector('.image-preview');
            imagePreview.style.backgroundImage = `url('${reader.result}')`;
            imagePreview.style.display = 'block';
        }
        reader.readAsDataURL(file);
    }
});

const productImage = document.getElementById('productImage');
const imagePreview = document.querySelector('.image-preview');
const removeButton = document.getElementById('removeButton');

productImage.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function() {
            imagePreview.style.backgroundImage = `url('${reader.result}')`;
            imagePreview.style.display = 'block';
            removeButton.style.display = 'block';
        }
        reader.readAsDataURL(file);
    }
});

removeButton.addEventListener('click', function() {
    imagePreview.style.backgroundImage = 'none';
    imagePreview.style.display = 'none';
    productImage.value = '';
    removeButton.style.display = 'none';
});

