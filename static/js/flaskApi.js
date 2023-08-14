$(document).ready(function () {
  $("#btnSubmit").click(function (e) {
    e.preventDefault();
    var form = $(this).closest('form');
    var apiRoute = form.data("api-route");
    // if(apiRoute == "/checkIn"){
    //     // Close the modal using the modal API
    //     var modal = new bootstrap.Modal(document.getElementById("checkInModal"));
    //     modal.hide(); // Close the modal
    // }
    var targetUrl = form.data("target-url"); // Get the target URL from the custom attribute
    var redirectUrl = targetUrl || "/"

    form.find(".btnSubmit").attr('disabled', 'disabled');

    $.post(apiRoute, form.serialize())
      .done(function (response) {
        // If form submission is successful, handle the response (e.g., redirect or show success message)
        if(apiRoute == "/login"){
          showMessage("Login successful.",'s')
        }
        else{
          showMessage("Data saved successfully.",'s')
        }
        
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

  $("#btnCheckIn").click(function (e) {
    e.preventDefault();

    var apiRoute = $(this).data("api-route");
 
   

    $.get(apiRoute)
      .done(function (res) {
       console.log(res)
       bindJSONToSelect(res.brands,"id","name","brand");
       bindJSONToSelect(res.types,"id","type","type");
       bindJSONToSelect(res.empty_locations,"id","name","location");
       bindJSONToSelect(res.discounts,"id","customer","discount");

       var checkInModal = document.getElementById("checkInModal");

       var modal = new bootstrap.Modal(checkInModal);
       modal.show();




      })
      .fail(function (error) {
        // If form submission fails, display the error in Bootstrap toaster
        showMessage(error.responseJSON?.error,'d')
      })
      .always(function() {
        

    });
  });

  $("#btnMove").click(function() {
    var brand = $(this).data("id");
    var location = $(this).data("location");

    console.log(brand,location)


   
});

$("#btnCheckOut").click(function() {
  var s = $(this).data("s");
  var sObject = JSON.parse(s);
  console.log("check button clicked with data:", sObject);
  // Your move logic here
});



  function bindJSONToSelect(jsonData, valuePropertyName, textPropertyName, selectId) {
  const selectElement = document.getElementById(selectId);

  if (!selectElement) {
    console.error(`Select element with ID ${selectId} not found.`);
    return;
  }

  selectElement.innerHTML = ""; // Clear existing options

  const defaultOption = document.createElement("option");
  defaultOption.disabled = true;
  defaultOption.selected = true;
  defaultOption.value = "";
  defaultOption.textContent = "Select One";
  selectElement.appendChild(defaultOption);

  for (const item of jsonData) {
    const option = document.createElement("option");
    option.value = item[valuePropertyName];
    option.text = item[textPropertyName];
    selectElement.appendChild(option);
  }
}


});






