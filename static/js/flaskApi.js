$(document).ready(function () {
  $("#btnSubmit").click(function (e) {
    e.preventDefault();
    var form = $(this).closest('form');
    var apiRoute = form.data("api-route");
    var targetUrl = form.data("target-url"); // Get the target URL from the custom attribute
    var redirectUrl = targetUrl || "/"

    form.find(".btnSubmit").attr('disabled', 'disabled');

    $.post(apiRoute, form.serialize())
      .done(function (response) {
        // If form submission is successful, handle the response (e.g., redirect or show success message)
        showMessage("Data saved successfully",'s')
        $("#btnSubmit")
        setTimeout(function() {
          window.location.href = redirectUrl; // Use the retrieved target URL for redirection
      }, 1000); // 1 seconds delay

      })
      .fail(function (error) {
        // If form submission fails, display the error in Bootstrap toaster
        showMessage(error.responseJSON?.error,'d')
      })
      .always(function() {
        form.find(".btnSubmit").removeAttr('disabled');


       
    });
  });

  function showMessage(message, type) {
    var alertType = ''
    switch (type) {
      case "d":
        alertType = 'danger'
        break;

      case "s":
        alertType = 'success'
        break;

      case "w":
        alertType = 'warn'
        break;

      default:
        break;
    }
    var alertHTML = `<div class="alert alert-${alertType}" role="alert">
      ${message}
    </div>`

    var alertContainer = $("#alert-container");
    alertContainer.append(alertHTML);

    setTimeout(function () {
      var alertElement = alertContainer.find(".alert");
      alertElement.remove();
    }, 30000);
  }

});






