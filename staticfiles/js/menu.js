$(document).ready(function() {
    // Shows Starters items when the page its loaded
    var defaultActive = $('.type-option[data-type="Starter"]');
    defaultActive.addClass('type-active');
    $('.filter-item').hide();
    $('.filter-item[data-type="Starter"]').show();
    $('.type-option').click(function() {
        // Get the type of the container clicked
        var type = $(this).data('type');
        $('.type-option').removeClass('type-active');
        $(this).addClass('type-active');
        // Hide all items
        $('.filter-item').hide();
        //Show the items with the same data-type as the type of the container clicked
        $('.filter-item[data-type="' + type + '"]').show();
    });
});