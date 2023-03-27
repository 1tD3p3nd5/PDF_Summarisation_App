
function displayResponse(response) {
    $("#summary").html(response);
    $("#process_pdf").prop("disabled", false); // Enable the button
    $("#processing_message").hide(); // Hide the processing message
}

$(document).ready(function () {
    $("#pdf_upload_form").submit(function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        $.ajax({
            url: "/upload",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function () {
                $("#process_pdf").prop("disabled", true); // Disable the button
                $("#processing_message").show(); // Show the processing message
            },
            success: function (data) {
                displayResponse(data.response);
            },
            error: function (xhr, textStatus, errorThrown) {
                alert("An error occurred while processing the PDF.");
                $("#process_pdf").prop("disabled", false); // Enable the button
                $("#processing_message").hide(); // Hide the processing message
            },
        });
    });
});



