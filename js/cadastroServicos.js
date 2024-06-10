$('#serviceImage').change(function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function () {
            $('.image-preview').css('background-image', `url('${reader.result}')`);
            $('.image-preview').css('display', 'block');
        }
        reader.readAsDataURL(file);
    }
});

$('#serviceImage').change(function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function () {
            $('.image-preview').css('background-image', `url('${reader.result}')`);
            $('.image-preview').css('display', 'block');
            $('#removeButton').css('display', 'block');
        }
        reader.readAsDataURL(file);
    }
});

$('#removeButton').click(function () {
    $('.image-preview').css('background-image', 'none');
    $('.image-preview').css('display', 'none');
    $('#serviceImage').val('');
    $(this).css('display', 'none');
});
