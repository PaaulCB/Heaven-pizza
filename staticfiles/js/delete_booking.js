$('#cancelModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);// Get the button that opened the modal
    var bookingId = button.data('booking-id'); // Extract the booking_id form the data-booking_id
    var deleteUrl = button.data('url').replace('9999', bookingId); //Get the url fron data-url and replace 9999 with bookingId
    $('#cancelConfirm').attr('href', deleteUrl);// Modify the action of the form
});