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