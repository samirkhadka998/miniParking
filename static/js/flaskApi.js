$(document).ready(function () {
  $(".btnSubmit").click(function (e) {
    e.preventDefault();
    var form = $(this).closest('form');
    console.log(form.serializeArray())
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
        if (apiRoute == "/login") {
          // showMessage("Login successful.", 's')
          showToast("Login successful.",'success')
        }
        else {
          // showMessage("Data saved successfully.", 's')
          showToast("Data saved successfully.",'success')

        }

        $("#btnSubmit")
        setTimeout(function () {
          window.location.href = redirectUrl; // Use the retrieved target URL for redirection
        }, 1000); // 1 seconds delay

      })
      .fail(function (error) {
        // If form submission fails, display the error in Bootstrap toaster
        // showMessage(error.responseJSON?.error, 'd')
        showToast(error.responseJSON?.error,'error')
      })
      .always(function () {
        form.find(".btnSubmit").removeAttr('disabled');



      });
  });


  function showToast(message, type) {
    toastr.options = {
        closeButton: true,
        progressBar: true,
        showMethod: 'slideDown',
        timeOut: 3000
    };
    toastr[type](message);
}
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
        bindJSONToSelect(res.brands, "id", "name", "brand");
        bindJSONToSelect(res.types, "id", "type", "type");
        bindJSONToSelect(res.empty_locations, "id", "name", "location");
        bindJSONToSelect(res.discounts, "id", "customer", "discount");

        var checkInModal = document.getElementById("checkInModal");

        var modal = new bootstrap.Modal(checkInModal);
        modal.show();




      })
      .fail(function (error) {
        // If form submission fails, display the error in Bootstrap toaster
        // showMessage(error.responseJSON?.error, 'd')
        showToast(error.responseJSON?.error,'error')

      })
      .always(function () {


      });
  });

  $(".btnMove").click(function () {
    var apiRoute = $(this).data("api-route");

    var checkIn = $(this).data("id");
    var location = $(this).data("location");
    var vehicle = $(this).data("vehicle");


    $.get(apiRoute)
      .done(function (res) {
        console.log(res)
        bindJSONToSelect(res.empty_locations, "id", "name", "movelocation");

    
        const moveHiddenCheckInId = document.getElementById('moveHiddenCheckInId');
        moveHiddenCheckInId.value = checkIn;

        const moveHiddenCurrentLocation = document.getElementById("moveHiddenCurrentLocation");
        moveHiddenCurrentLocation.value = location;

        const moveCurrentLocation = document.getElementById("moveCurrentLocation"); 
        moveCurrentLocation.value = location;

        const moveTitle = document.getElementById('moveModalLabel');
        moveTitle.innerHTML = `${vehicle} <span class="form-control-sm">Move</span>`


    
        var modal = new bootstrap.Modal(moveModal);
        modal.show();




      })
      .fail(function (error) {
        // If form submission fails, display the error in Bootstrap toaster
        // showMessage(error.responseJSON?.error, 'd')
        showToast(error.responseJSON?.error,'error')

      })
      .always(function () {


      });


   



  });

  $(".btnCheckOut").click(function () {
    //checkOutModal
    var vehicle = $(this).data("vehicle");
    var checkIn = $(this).data("id");
    var location = $(this).data("location");
    var fee = $(this).data("fee");
    const checkInInput = document.getElementById('checkInId');
    checkInInput.value = checkIn;
    const locationInput = document.getElementById('cLocation');
    locationInput.value = location;
    const locationDisplay = document.getElementById('locationDisplay');
    locationDisplay.value = location

    const checkOutModalLabel = document.getElementById('checkOutModalLabel');
    checkOutModalLabel.innerHTML = `<b class="text-bg-danger p-1"> ${vehicle} </b><span class="col-form-label-sm mx-2 p-1">Check Out</span>`;
    var modal = new bootstrap.Modal(checkOutModal);
    modal.show();
    
    const amountInput = document.getElementById('amount');
    const unpaidRadioButton = document.getElementById('UnPaid');
    const paidRadioButton = document.getElementById('Paid');

    amountInput.value = fee;
    
    unpaidRadioButton.addEventListener('change', (event) => {
      if (event.target.checked) {
        amountInput.value = "";
        amountInput.setAttribute('disabled', 'true');
      } else {
        amountInput.removeAttribute('disabled');
      }
    });
  
    paidRadioButton.addEventListener('change', (event) => {
      if (event.target.checked) {
        amountInput.value = fee;
        amountInput.removeAttribute('disabled');
      } else {
        amountInput.setAttribute('disabled', 'true');
      }
    });
   

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
      if(selectId == "discount")
      {
        option.text = `${item.customer} - ${item.percentage}%`;
      }
      else{
        option.text = item[textPropertyName];
      }
      selectElement.appendChild(option);
    }
  }

 

});






