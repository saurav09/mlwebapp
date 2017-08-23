$(document).ready(function () {
    $('button').click(function (e) {
        var url = "{{ url_for('something') }}"; // send the form data here.
        var url1 = "/something/"
        $.ajax({
            type: "POST",
            url: url1,
            data: $('form').serialize(), // serializes the form's elements.
            success: function (data) {
                console.log(data)  // display the returned data in the console.
            }
        })
            .done(function (data) {
                $('#prediction').text(data.prediction).show();
            });
        e.preventDefault(); // block the traditional submission of the form.
    });
    // Inject our CSRF token into our AJAX request.
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
            }
        }
    })
});