$(function () {
    $(".cipher-btn").on({
        click: function () {
            const value = $(".input-field").val();
            const cipher_url = $(this).data("cipher");
            cipher(value, cipher_url);
        }
    });
});

function cipher(input, cipher_url) {
    $.ajax({
        type: "GET",
        url: cipher_url,
        data: { text: input },
        contentType: "application/json",

        success: function (response) {
            $(".output-field").text(response.output);
            $(".learn-section").html(response.steps);
            window.MathJax.typeset();
        },

        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log("XMLHttpRequest: " + XMLHttpRequest + "\nStatus: " + textStatus + "\nError: " + errorThrown);
        }
    });
}
