$(function () {
    $("[name=output-field]").val("");
    $("#copy-btn").hide();

    $(".hill-cipher-btn").on({
        click: function () {
            $("#key-field").removeClass("is-invalid");
            $(".learn-section").html("");
            $("[name=output-field]").val("");

            const message = $("[name=message-field]").val().toUpperCase();
            const key = $("[name=key-field]").val().toUpperCase();
            const keysize = $("[name=keysize]:checked").val();
            const mode = $(this).data("mode");

            $.ajax({
                type: "GET",
                url: "api/hill-cipher",
                data: { message, key, keysize, mode },
                contentType: "application/json",

                success: function (response) {
                    $("[name=output-field]").val(response.output);
                    $("#copy-btn").show();

                    fetch("render-subtemplate")
                        .then(response => response.text())
                        .then(renderedHtml => {
                            $(".learn-section").html(renderedHtml);
                            window.MathJax.typeset();
                        })
                        .catch(error => console.error("Error:", error));
                },

                error: function (xhr) {
                    let errorJSON = JSON.parse(xhr.responseText);
                    console.log(errorJSON);

                    $("#key-field").addClass("is-invalid");
                    $("#key-error").text(errorJSON.message);
                }
            });
        }
    });

    var timeout;

    $("#copy-btn").on({
        click: function () {
            const messageField = $("[name=message-field]");
            messageField.val($("[name=output-field]").val());

            messageField.removeClass("highlight");

            setTimeout(function () {
                messageField.addClass("highlight");
            }, 60);

            if (timeout) {
                clearTimeout(timeout);
            }

            timeout = setTimeout(function () {
                messageField.removeClass("highlight");
            }, 1000);
        }
    });
});


$(function () {
    $("#rsa-generate-keys-btn").on({
        click: function () {
            $("#prime-p").removeClass("is-invalid");
            $("#prime-q").removeClass("is-invalid");

            let p = $("#prime-p").val();
            let q = $("#prime-q").val();

            // p = (p !== null && p !== undefined) ? parseInt(p) : null;
            // q = (q !== null && q !== undefined) ? parseInt(q) : null;

            // console.log({ p, q });

            $.ajax({
                url: "/rsa_generate_keys",
                type: "POST",
                data: JSON.stringify({ p, q }),
                contentType: "application/json",

                success: function (response) {
                    $("#prime-p").val(response.p);
                    $("#prime-q").val(response.q);

                    $("[name=public-key").val("(" + response.public_key[0] + ", " + response.public_key[1] + ")");
                    $("[name=private-key").val("(" + response.private_key[0] + ", " + response.private_key[1] + ")");
                },

                error: function (xhr) {
                    // console.log(xhr.responseText)
                    let errorJSON = JSON.parse(xhr.responseText);
                    // console.log(errorJSON);

                    for (let key in errorJSON) {
                        for (let error in errorJSON[key]) {
                            // console.log("key msg: " + error);
                            $("#prime-" + key).addClass("is-invalid");
                            $("#error-" + key).text(errorJSON[key][error])
                        }
                    }
                    window.MathJax.typeset();
                }
            });
        }
    });

    $("#rsa-encrypt-btn").on({
        click: function () {
            const message = $("[name=message-field]").val();
            const key = $("[name=key-field]").val();
            console.log("message: " + message);
            console.log(key);

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

                error: function (xhr, textStatus, errorThrown) {
                    console.log("xhr: " + xhr + "\nStatus: " + textStatus + "\nError: " + errorThrown);
                }
            });
        }
    });

    $("#rsa-decrypt-btn").on({
        click: function () {
            const message = $("[name=message-field]").val().toUpperCase();
            const key = $("[name=key-field]").val().toUpperCase();
            console.log(message);
            console.log(key);

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

                error: function (xhr, textStatus, errorThrown) {
                    console.log("xhr: " + xhr + "\nStatus: " + textStatus + "\nError: " + errorThrown);
                }
            });
        }
    });
});
