$('#modifyModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);// Get the button that opened the modal
    var bookingId = button.data('booking-id'); // Extract the booking_id form the data-booking_id
    var modifyUrl = button.data('url').replace('9999', bookingId); //Get the url fron data-url and replace 9999 with bookingId
    $('#booking-form').attr('action', modifyUrl);// Modify the action of the form
    // Get the data to prefield from the data atribute of the button that opened the modal 
    var bookingName = button.data('booking-name');
    var numberOfGuests = button.data('number-of-guests');
    var bookingDate = button.data('booking-date');
    var bookingTime = button.data('booking-time');
    var childChair = button.data('child-chair') === 'True';
    var allergies = button.data('allergies');
    var tablePreferences = button.data('table-preferences');
    // FIll the value of the form fields with the ones getted above 
    var form = $(this);
    form.find('#booking_name').val(bookingName);
    form.find('#number_of_guests').val(numberOfGuests);
    form.find('#booking_date').val(bookingDate);
    form.find('#booking_time').val(bookingTime);
    form.find('#child_chair').prop('checked', childChair);
    form.find('#allergies').val(allergies);
    form.find('#table_preferences').val(tablePreferences);
    $('#find-table-btn').data('booking-id',bookingId)
});
$('#modifyModal').on('hidden.bs.modal', function () {
    // Reset booking-result after closing a modal
    $('#booking-results').html('');
});