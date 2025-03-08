$(function () {
    $("#hill-cipher-btn").on({
        click: function () {
            const message = $("[name=message-field]").val().toUpperCase();
            const key = $("[name=key-field]").val().toUpperCase();
            console.log(message);
            console.log(key);
            callHillCipher(message, key);
        }
    });
});

function callHillCipher(message, key) {
    $.ajax({
        type: "GET",
        url: "hill-cipher",
        data: { message: message, key: key },
        contentType: "application/json",

        success: function (response) {
            $("[name=output-field]").text(response.output);
            $(".learn-section").html(response.template);
            window.MathJax.typeset();
        },

        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log("XMLHttpRequest: " + XMLHttpRequest + "\nStatus: " + textStatus + "\nError: " + errorThrown);
        }
    });
}
