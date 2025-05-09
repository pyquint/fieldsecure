function encipher(endpoint, payload) {
    $.ajax({
        type: "GET",
        url: endpoint + "/cipher",
        data: payload,
        contentType: "application/json",

        success: function (response) {
            $("#learn-section").html(response);
            window.MathJax.typeset();

            const outputField = $("[name=output-field]");
            const output = $("#output-data").data("output");
            outputField.val(output);

            $(".copy-btn").show();

            scrollTop(outputField, 16);
        },

        error: (xhr) => displayXhrJsonError(xhr)
    });
}

function scrollTop(element, offset) {
    $('html, body').animate({
        scrollTop: element.offset().top - offset
    }, 500);
}

function displayXhrJsonError(xhr) {
    let errors = JSON.parse(xhr.responseText);
    console.error(errors);

    for (let field in errors) {
        $("input[name=" + field + "]").addClass("is-invalid");
        $("#error-" + field).text(errors[field]);
    }

    window.MathJax.typeset();
}

function resetCiphersPageState() {
    $("#learn-section").html("");
    $("[name=output-field]").val("");

    const keys = $(".key-field").toArray();
    keys.forEach((key) => {
        key.classList.remove("is-invalid");
    });
}

// HILL CIPHER
$(function () {
    $("[name=output-field]").val("");

    $("#hill-cipher .cipher-btn").on({
        click: function () {
            resetCiphersPageState();

            const message = $("[name=message-field]").val();
            const key = $("[name=key]").val();
            const keysize = $("[name=keysize]:checked").val();
            const mode = $(this).data("mode");

            const payload = { message, key, keysize, mode };
            encipher("hill-cipher", payload);
        }
    });
});

// ATBASH
$(function () {
    $("[name=output-field]").val("");

    $("#atbash-cipher .cipher-btn").on({
        click: function () {
            resetCiphersPageState();

            const message = $("[name=message-field]").val();

            const payload = { message };
            encipher("atbash-cipher", payload);
        }
    });
});

// RSA
$(async function () {
    let keys = await generateKeys();

    function clearPrimeFields() {
        $("[name=p]").val("");
        $("[name=q]").val("");
        $("[name=e]").val("");
    }

    function generateKeys(p = null, q = null, e = null) {
        resetCiphersPageState();
        clearPrimeFields();

        return $.ajax({
            url: "rsa/generate_keys",
            type: "GET",
            data: { p, q, e },
            contentType: "application/json",

            error: (xhr) => displayXhrJsonError(xhr)
        });
    };

    $("#rsa-generate-keys-btn").on({
        click: async function () {
            keys = await generateKeys();

            // (n, e), (n, d)
            $("#p").val(keys.p);
            $("#q").val(keys.q);
            $("#e").val(keys.public_key[1]);

            const publicKey = "(" + keys.public_key[0] + ", " + keys.public_key[1] + ")";
            const privateKey = "(" + keys.private_key[0] + ", " + keys.private_key[1] + ")";

            $("[name=public-key").val(publicKey);
            $("[name=private-key").val(privateKey);

            window.MathJax.typeset();
        }
    });

    $("#rsa .cipher-btn").on({
        click: function () {
            if (keys) {
                let cipherBtn = $(this);
                const message = $("[name=message-field]").val();
                const mode = cipherBtn.data("mode");

                let p = $("#p").val();
                let q = $("#q").val();

                // console.log("message: " + message);
                // console.log(JSON.stringify(keys));

                const payload = { message, p, q, keys: JSON.stringify(keys), mode };
                encipher("rsa", payload);

            } else {
                console.error("No keys, generate first.");
            }
        }
    });
});

$(function () {
    const copyButton = $(".copy-btn");
    copyButton.hide();
    var timeout;

    copyButton.on({
        click: function () {
            const messageField = $(".message-field");

            scrollTop($("label[for='message-field']"), 16);

            messageField.val($(".output-field").val());

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
