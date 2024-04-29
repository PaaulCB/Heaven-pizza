export function updateDateTimeMin() {
    // Function to get the date and time now and show it on the relatives form fields
    var now = new Date();
    var day = ("0" + now.getDate()).slice(-2);
    var month = ("0" + (now.getMonth() + 1)).slice(-2);
    var year = now.getFullYear();
    var hour = ("0" + now.getHours()).slice(-2);
    var minute = ("0" + now.getMinutes()).slice(-2);

    var currentDate = year + "-" + month + "-" + day;
    var currentTime = hour + ":" + minute;

    $('#booking_date').val(currentDate);
    $('#booking_time').val(currentTime);
}