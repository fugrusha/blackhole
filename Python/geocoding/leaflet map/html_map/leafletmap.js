window.onload = function () {
    var basemap = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
		attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	});

    $.getJSON("geo.geojson", function(data) {

    var geojson = L.geoJson(data, {
      onEachFeature: function (feature, layer) {
        layer.bindPopup('<p><b>ID TT:</b> ' + feature.properties.ID_TT + '</p>' + '<p><b>Client:</b> ' + feature.properties.Client + '</p>' + '<p><b>Address:</b> ' +  feature.properties.Address + '</p>' + '<p><b>Coordinates:</b> ' + feature.geometry.coordinates + '</p>');
      }
    });


    var map = L.map('my-map')
    .fitBounds(geojson.getBounds());

    basemap.addTo(map);
    geojson.addTo(map);
  });

};
