function initMap() {
  // Create a map object and specify the DOM element for display.
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    scrollwheel: false,
    zoom: 8
  });
}

$(document).on('ready page:load', function() {

  var map, markers = [];
  var data_lines = image_data.split('\n');
  function initMap() {
    // Create a map object and specify the DOM element for display.
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: -34.397, lng: 150.644},
      scrollwheel: true,
      zoom: 5
    });
  }

  var maxLat = -100, minLat = 100, maxLng = -200, minLng = 200;
  var maxDate = new Date(1900,1,1), minDate = new Date(2500,12,12);

  $('[data-toggle="datepicker"]').datepicker({
    format : 'yyyy-mm-dd',
    language : 'ko-KR'
  });

  var refreshTable = function() {
    for (var i = 0; i < markers.length; i++ ) {
      markers[i].setMap(null);
    }
    markers.length = 0;
    $('tbody').html('');
  }

  var fillTable = function(lines) {
    lines.forEach(function(line) {
      if( typeof(line) == "string" )
        var row = line.split(',');
      else
        var row = line;

      if( row[1] ) {
        var date = row[1].split(' ')[0].replace(':','-')
        var tmpDate = new Date(date);
        if( minDate > tmpDate ) {
          minDate = tmpDate;
        }
        if( maxDate < tmpDate ) {
          maxDate = tmpDate;
        }
      }

      if( row[2] && row[3] ) {
        var lat = parseFloat(row[2]), lng = parseFloat(row[3]);
        if( maxLat < lat ) maxLat = lat;
        if( minLat > lat ) minLat = lat;
        if( maxLng < lng ) maxLng = lng;
        if( minLng > lng ) maxLng = lng;
      }

      if( date ) {

        $('tbody').append(
          "<tr>" +
            "<td>" + row[0] + "</td>" +
            "<td>" + row[1] + "</td>" +
            "<td>" + row[2] + "</td>" +
            "<td>" + row[3] + "</td>" +
          "</tr>"
        );

        var infoWindow = new google.maps.InfoWindow({
          content: '<a href="./images/' + row[0] + '" target="_blank">사진 보기</a>' +
            '<p>' + row[1] + '</p>' +
            '<p>' + row[2] + '</p>' +
            '<p>' + row[3] + '</p>'
        });
        var marker = new google.maps.Marker({
          map: map,
          position: {
            lat : parseFloat(row[2]),
            lng : parseFloat(row[3])
          },
          title: row[0]
        });
        marker.addListener('click', function() {
          infoWindow.open(map, marker);
        });
        markers.push(marker);
      }
    });

    map.setCenter(new google.maps.LatLng( (minLat+maxLat)/2, (minLng+maxLng)/2 ));
  }

  var setDateRange = function() {
    $('#start-date').datepicker('setDate',minDate);
    $('#end-date').datepicker('setDate',maxDate);
  }

  $('#filter').on('click', function() {
    var filterStartDate = $('#start-date').datepicker('getDate');
    var filterEndDate = $('#end-date').datepicker('getDate');

    var filteredLines = [];
    data_lines.forEach(function(line) {
      var row = line.split(',');

      if( row[1] ) {
        var date = row[1].split(' ')[0].replace(':','-');
        var tmpDate = new Date(date);

        if( filterStartDate <= tmpDate && tmpDate <= filterEndDate )
          filteredLines.push(row);
      }
    });

    refreshTable();
    fillTable(filteredLines);
  });

  initMap();
  refreshTable();
  fillTable(data_lines);
  setDateRange();

});
