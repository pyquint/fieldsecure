# Ciphers Page
## Adding New Pages
In Visual Studio Code, I have defined a snippet such that one only need to select the "Ciphers template" snippet by typing `cipher-template` in order to populate a template for a new ciphers page. It is then up to the developer how to style the page, following the block order.

### Currently defined blocks
- **Informational** - metadata and content regarding the cipher
    - `title` - page title
    - `header` - title header
    - `desc` - cipher description
    - `learn_section` - container to be populated with the appropriate subtemplate after encipherment ("learn" subtemplates are found in `templates/learn`)
- **Functional** - elements that implements the cipher itself and which the user interacts
    - `input` - how the cipher accepts input (ex. textbox)
    - `keys` - what keys the cipher utilizes and how (omit if none)
    - `buttons` - how the cipher initiates the encipherment (ex. buttons)
    - `output` -  how the cipher displays the output (ex. textbox)
- **Extra** - for further customization or adding JavaScript magic
    - `style`
    - `script`

## Components
The blocks mentioned above are wrapped in simple non-styled divs with an id the same as the block name for semantic purposes only. The developer must create and style the elemenets themselves, which allows them flexibility in designing and implementing the ciphers page to their likings and needs.

For convenience, there are pre-defined encipherment components located in the `components` subdirectory. To use these components, add an `include` statement in the HTML document.

e.g. `components/cipherBtn.html`:
```html
<div class="float-end">
    <button class="btn btn-warning cipher-btn" id="cipher-btn">Cipher</button>
</div>
```

To use:
```jinja
{% include "components/cipherBtn.html" %}
```

A VSCode snippet is available to easily add these components, just type `component` and select "Include UI component".

## Enciphering
### Functional Components
The enciphering button, whether to `encrypt`, `decrypt`, or simply `cipher` (should the encryption is the same as decryption), must have the  `{{ encipher }}-btn` id.

For encryption and decryption must have `data-mode` assigned to either `"encrypt"` or `"decrypt"`.

Should the cipher necessitates unconventional input, textbox, or button element, copy the important attributes above or from the pre-defined [Components](Docs.md#Components).

### Keys
Keys for the cipher, if present, must have an accompanying `.invalid-feedback` div, with an id name that follows the format `error-{{ name }}`, where `name` is input box's `name` attribute.

```html
<input name="key" class="key-field form-control" type="text" autocapitalize="on" />
<div id="error-key" class="invalid-feedback">Key matrix is not invertible.</div>
```

### JavaScript Logic
To hook the encipher function, simply imiate the following code:
```javascript
$(function () {
    $("[name=output-field]").val("");

    $("#{{ cipher_endpoint }} .cipher-btn").on({
        click: function () {
            resetCiphersPageState();

            // example arguments
            const message = $("[name=message-field]").val();
            const key = $("[name=key]").val();
            const keysize = $("[name=keysize]:checked").val();
            const mode = $(this).data("mode");

            const payload = { message, key, keysize, mode };
            encipher("{{ cipher_endpoint }}", payload);
        }
    });
});
```

`{{ cipher_endpoint }}` must match with the value assigned to the `cipher_endpoint` argument defined when rendering the current cipher view:

```python
return render_template("ciphers/atbash_cipher.html", cipher_endpoint="atbash-cipher")
```

(The whole cipher subtemplate is wrapped around a `#{{ cipher_endpoint }}` div.)


## Displaying Output
Currently, the output is stored by rendering it in a data div (see `learn/__output_data.html`) that **must be included inside each "learn" subtemplates**.

```html
<div id="output-data" data-output="{{ output }}"></div>
```

From which the value for the output textbox is retrieved and displayed after encipherment.

```javascript
const outputField = $("[name=output-field]");
const output = $("#output-data").data("output");
outputField.val(output);
```

## Error Handling
When returning an error message directed to an key field due to invalid field data, indicate the field's key name in order for the message to be displayed correctly on the client side.

e.g.

Server-side:

```python
return jsonify({"key": "Key must be letters only."}), 400
```

Client-side:
>The error div's `id` must be in format `error-{name}`.

```html
<input name="key" class="key-field form-control" type="text" autocapitalize="on" />

<div id="error-key" class="invalid-feedback"></div>
```

```javascript
for (let key in errorJSON) {
    $("input[name=" + key + "]").addClass("is-invalid");
    $("#error-" + field).text(errorJSON[key]);
}
```

The error message should be displayed under the `input` element with `name="key"`.
