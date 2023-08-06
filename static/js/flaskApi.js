$(document).ready(function() {
  $(document).on("submit", "form", function (e) {
    e.preventDefault();
    var form = $(this);
    var apiRoute = form.data("api-route");
  
    $.post(apiRoute, form.serialize())
        .done(function (response) {
            // If form submission is successful, handle the response (e.g., redirect or show success message)
            // For example, if it's the login form, you can redirect to the home page.
            // window.location.href = "/";
        })
        .fail(function (error) {
            // If form submission fails, display the error in Bootstrap toaster
            showError(error.responseJSON?.error)
        });
  });
  
  function showError(message, type = 'danger') {
      var alertHTML = `<div class="alert alert-${type}" role="alert">
      ${message}
    </div>`
  
      var alertContainer = $("#alert-container");
      alertContainer.append(alertHTML);

      setTimeout(function() {
        var alertElement = alertContainer.find(".alert");
        alertElement.remove();
      }, 3000);
  }
  
});


