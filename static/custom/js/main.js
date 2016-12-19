var map;
var markers = [];
var my_markers = [];
var lngs = [];
var lats = [];
var events_names = [];
var events_descriptions = [];
var events_organizers = [];
var events_statuses = [];
var events_on_map = [];

// document.onready = function () {
//   document.querySelectorAll("input[required]").forEach(function (e) {
//     //  .mdl-textfield.is-invalid
//     console.log(e);
//      e.required = true;
//   });
// };



function initMap() {
  var haightAshbury = {lat: 55.75222, lng: 37.61556};
  var zoom;

  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 17,
    center: haightAshbury,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  });

  for (var i = 0; i < lngs.length; i++) {
    var myLatlng = {lat: lats[i], lng: lngs[i]};
    var marker = new google.maps.Marker({
      position: myLatlng,
      map: map
    });
    markers.push(marker);
    markers[i].setMap(map);
    var contentString = '<div class="demo-card-wide mdl-card mdl-shadow--2dp">'+
                        '<div class="mdl-card__title mdl-card--expand">'+
                        '<h2 class="mdl-card__title-text">'+ events_names[i] +'</h2>'+
                        '</div>'+
                        '<div class="mdl-card__supporting-text">'+
                        '<b>Организатор:</b> ' + events_organizers[i] + '</br>' + events_descriptions[i]+
                        '</div>'+
                        '<div class="mdl-card__actions mdl-card--border">'+
                        '<input type="button" id="join_event" class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect" value="Enviar Mail">  '
                        '</div>'+
                        '<div class="mdl-card__menu">'+
                        '<button class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect">'+
                        '<i class="material-icons">share</i>'+
                        '</button>'+
                        '</div>'+
                        '</div>';
    addInfoWindow(marker, contentString)
  }

  map.addListener('click', function(event) {
    addMarker(event.latLng);
  });

}


function addInfoWindow(marker, message) {
  var infoWindow = new google.maps.InfoWindow({
    content: message
  });
  google.maps.event.addListener(marker, 'click', function () {
    infoWindow.open(map, marker);
    document.getElementById("join_event").addEventListener("click", function(){
      join_event();
    });
  });
}


function addMarker(location) {
  var marker = new google.maps.Marker({
    position: location,
    map: map
  });
  if (my_markers.length > 0) {
    del_marker = my_markers[my_markers.length-1];
    del_marker.setMap(null);
    my_markers.pop();
  } else {
  }
  my_markers.push(marker);
  var contentString = '<div class="demo-card-wide mdl-card mdl-shadow--2dp">'+
                      '<div class="mdl-card__title mdl-card--expand">'+
                      '<h2 class="mdl-card__title-text">'+ document.getElementById("event_name").value +'</h2>'+
                      '</div>'+
                      '<div class="mdl-card__supporting-text">'+
                      document.getElementById("event_description").value+
                      '</div>'+
                      '<div class="mdl-card__actions mdl-card--border">'+
                      '<button id="join_event" class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect">'+
                      'Присоединиться'+
                      '</button>'+
                      '</div>'+
                      '<div class="mdl-card__menu">'+
                      '<button class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect">'+
                      '<i class="material-icons">share</i>'+
                      '</button>'+
                      '</div>'+
                      '</div>';
  addInfoWindow(marker, contentString);

  document.getElementById("event_location").value = location;
  var attribute = document.getElementById("label_event_location").getAttribute("class");
  // document.getElementById("label_event_location").setAttribute("class", attribute + "is-dirty is-upgraded");
  document.getElementById("label_event_location").setAttribute("class", "mdl-textfield mdl-js-textfield mdl-textfield--floating-label is-dirty is-upgraded");

}

function join_event() {
  $.ajax({
    url : "join_event/", // the endpoint
    type : "POST", // http method
    data : {
      // username : $('#username').val(),
      // password : $('#password').val(),
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    }, // data sent with the post request

    // handle a successful response
    success : function(json) {
      console.log('ok');
      // location.reload();
    },
    // handle a non-successful response
    error : function(xhr,errmsg,err) {
      // display_form_errors(xhr.responseText, $('#login-form'));
      console.log('not ok');
    },
  });
}
