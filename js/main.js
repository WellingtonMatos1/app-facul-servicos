$(document).ready(function () {
    $('#navbar').load('/navbar.html', () => {
        if (localStorage.getItem('access_token') != null) {
            $("#cadastroServico").show();
        }

        $("#linkVoltar").click(() => {
            window.history.back();
        });
    });

    $("#footer").load("/footer.html", () => {
        if (localStorage.getItem('access_token') != null) {
            $("#cadastroServico").attr("href", "/cadastroServico.html");
            $("#cadastroServico").html('<i class="fas fa-plus-circle"></i>');
        }
    });
});

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}