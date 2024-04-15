function initMap(){
    var coordinates = { lat: 51.50721651364372, lng: -0.041644376581566916 };
    var map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: coordinates
    });
    var marker = new google.maps.Marker({
        position: coordinates,
        map: map,
        title: "Heaven Pizza"
    });
}