import {
    updateDateTimeMin
} from './update_datetime.js';
$(document).ready(function () {
    updateDateTimeMin();
    // Disable the Enter to send the form
    $(window).keydown(function (event) {
        if (event.keyCode == 13) {
            event.preventDefault();
            return false;
        }
    });
    $('#booking-form').on('submit', function (event) {
        var button = $(document.activeElement).val();
        if (button === 'find_table') {
            event.preventDefault();
            // Delete the content on booking-results
            $('#booking-results').html('');

            var now = new Date();
            var day = ("0" + now.getDate()).slice(-2);
            var month = ("0" + (now.getMonth() + 1)).slice(-2);
            var year = now.getFullYear();
            var hour = ("0" + now.getHours()).slice(-2);
            var minute = ("0" + now.getMinutes()).slice(-2);

            var currentDate = year + "-" + month + "-" + day;
            var currentTime = hour + ":" + minute;
            var currentDateTime = new Date(currentDate + 'T' + currentTime);

            var userDate = $('#booking_date').val()
            var userTime = $('#booking_time').val()
            var userDateTime = new Date(userDate + 'T' + userTime);
            if (userDateTime < currentDateTime) {
                $('#booking-results').html('<p class="text-center">You can only book a table for the future, please enter a valid date and time<br> Current date: ' + currentDate + ' Current time: ' + currentTime);
            } else {


                var booking_id = $(document.activeElement).data('booking-id')
                $.ajax({
                    type: 'POST',
                    url: '/booking/',
                    data: $(this).serialize() + '&csrfmiddlewaretoken=' + $('input[name="csrfmiddlewaretoken"]').val() + '&booking_id=' + booking_id,
                    success: function (response) {
                        if (response.available) {
                            $('#booking-results').html(
                                '<p>Table available!</p>' +
                                '<input type="hidden" name="table_id" value="' + response.table_id + '">' +
                                '<button type="submit" name="form-button" value="make-booking" class="btn btn-book">Book Now</button>'
                            );
                        } else {
                            let content = '<p>No tables available at the selected time.</p><p>These are the next available times:</p>';
                            response.alternatives.forEach((alt, index) => {
                                content += `<input type="hidden" name="book-option-${index + 1}-time" value="${alt.time}">` +
                                    `<input type="hidden" name="book-option-${index + 1}-table_id" value="${alt.table_id}">` +
                                    `<button type="submit" name="form-button" value="book-option-${index + 1}" class="btn btn-book m-1">Book on<br>${alt.time}</button>`;
                            });
                            $('#booking-results').html(content);
                        }
                    },
                    error: function () {
                        $('#booking-results').html('<p>Error checking table availability.</p>');
                    }
                });
            }
        }
    });
    // If the user changes any of the fields relevants for the availability delete the booking-results
    $('#number_of_guests').on('input', function () {
        $('#booking-results').html('');
    });
    $('#booking_date, #booking_time').on('change', function () {
        $('#booking-results').html('');
    });
});