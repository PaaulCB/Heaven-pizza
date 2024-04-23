$(document).ready(function() {
    // Disable the Enter to send the form
    $(window).keydown(function(event){
        if(event.keyCode == 13) {
          event.preventDefault();
          return false;
        }
      });
    $('#booking-form').on('submit', function(event) {
        var button = $(document.activeElement).val();
        if (button === 'find_table') {
            event.preventDefault();
            // Delete the content on booking-results
            $('#booking-results').html('');
            $.ajax({
                type: 'POST',
                url: '/booking/',
                data: $(this).serialize() + '&csrfmiddlewaretoken=' + $('input[name="csrfmiddlewaretoken"]').val(),
                success: function(response) {
                    if (response.available) {
                        $('#booking-results').html(
                            '<p>Table available!.</p>' +
                            '<input type="hidden" name="table_id" value="' + response.table_id + '">' +
                            '<button type="submit" name="form-button" value="make-booking" class="btn btn-success">Book Now</button>'
                        );
                    } else {
                        $('#booking-results').html(
                            '<p>No tables available at the selected time.</p>' +
                            '<p>This are the next availables times </p>'+
                            '<input type="hidden" name="option-1-time" value="' + response.alternatives[0].time + '">' +
                            '<input type="hidden" name="option-1-table_id" value="' + response.alternatives[0].table_id + '">' +
                            '<button type="submit" name="form-button" value="book-option-1" class="btn btn-success">'+ response.alternatives[0].time +'</button>'+
                            '<input type="hidden" name="option-2-time" value="' + response.alternatives[1].time + '">' +
                            '<input type="hidden" name="option-2-table_id" value="' + response.alternatives[1].table_id + '">' +
                            '<button type="submit" name="form-button" value="book-option-2" class="btn btn-success">'+ response.alternatives[1].time +'</button>'+
                            '<input type="hidden" name="option-3-time" value="' + response.alternatives[2].time + '">' +
                            '<input type="hidden" name="option-3-table_id" value="' + response.alternatives[2].table_id + '">' +
                            '<button type="submit" name="form-button" value="book-option-3" class="btn btn-success">'+ response.alternatives[2].time +'</button>'
                        );
                    }
                },
                error: function() {
                    $('#booking-results').html('<p>Error checking table availability.</p>');
                }
            });
        }
    });
});