$(function () {
    $("#hill-cipher-btn").on({
        click: function () {
            $(".learn-section").html("");
            const message = $("[name=message-field]").val().toUpperCase();
            const key = $("[name=key-field]").val().toUpperCase();
            const k = $("[name=k]").val();
            encryptWithHillCipher({ message, key, k });
        }
    });

    $("#rsa-cipher-btn").on({
        click: function () {
            const message = $("[name=message-field]").val().toUpperCase();
            const key = $("[name=key-field]").val().toUpperCase();
            console.log(message);
            console.log(key);
            encryptWithRSA(message, key);
        }
    });
});


function encryptWithHillCipher(params) {
    $.ajax({
        type: "GET",
        url: "api/hill-cipher",
        data: params,
        contentType: "application/json",

        success: function (response) {
            $("[name=output-field]").text(response.output);

            fetch("render-subtemplate")
                .then(response => response.text())
                .then(renderedHtml => {
                    $(".learn-section").html(renderedHtml);
                    window.MathJax.typeset();
                })
                .catch(error => console.error("Error:", error));
        },

        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log("XMLHttpRequest: " + XMLHttpRequest + "\nStatus: " + textStatus + "\nError: " + errorThrown);
        }
    });
}

function encryptWithRSA(message, key) {
    $.ajax({
        type: "GET",
        url: "/api/rsa",
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
