$(function () {
    // HILL CIPHER
    $("[name=output-field]").val("");

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
                    $(".copy-btn").show();

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
});


$(function () {
    // RSA
    let keys;

    function generateKeys() {
        return new Promise(function (resolve, reject) {
            $("#prime-p").removeClass("is-invalid");
            $("#prime-q").removeClass("is-invalid");

            let p = $("#prime-p").val();
            let q = $("#prime-q").val();

            $.ajax({
                url: "/rsa_generate_keys",
                type: "POST",
                data: JSON.stringify({ p, q }),
                contentType: "application/json",

                success: function (response) {
                    // response public key = (n, e)f
                    // response private key = (n, d)

                    $("#prime-p").val(response.p);
                    $("#prime-q").val(response.q);

                    $("[name=public-key").val("(" + response.public_key[0] + ", " + response.public_key[1] + ")");
                    $("[name=private-key").val("(" + response.private_key[0] + ", " + response.private_key[1] + ")");

                    keys = response;
                    resolve(true);
                },

                error: function (xhr) {
                    // console.log(xhr.responseText)
                    let errorJSON = JSON.parse(xhr.responseText);
                    for (let key in errorJSON) {
                        for (let error in errorJSON[key]) {
                            // console.log("key msg: " + error);
                            $("#prime-" + key).addClass("is-invalid");
                            $("#error-" + key).text(errorJSON[key][error]);
                        }
                    }

                    window.MathJax.typeset();
                    reject(true);
                }
            });
        });
    }

    $("#rsa-generate-keys-btn").on({
        click: generateKeys
    });

    $(".rsa-cipher-btn").on({
        click: function () {
            generateKeys().then(function () {
                const message = $("[name=message-field]").val();
                const mode = $(this).data("mode");

                console.log("message: " + message);
                console.log(JSON.stringify(keys));

                $.ajax({
                    type: "GET",
                    url: "/api/rsa",
                    data: { message, keys: JSON.stringify(keys), mode },
                    contentType: "application/json",

                    success: function (response) {
                        $("[name=output-field]").val(response.output);
                        $(".copy-btn").show();

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
            });
        }
    });
});

$(function () {
    const copyButton = $(".copy-btn");
    copyButton.hide();
    var timeout;

    copyButton.on({
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
