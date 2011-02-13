var initialLocation = null;
var currentLocation = null;
var clujNapoca = new google.maps.LatLng(46.7667, 23.6);
var browserSupportFlag = new Boolean();
var map = null;
var userLocationPushpin = null;

function initialize_your_location() {
	var myOptions = {
		zoom : 10,
		mapTypeId : google.maps.MapTypeId.ROADMAP
	};
	map = new google.maps.Map(document.getElementById("map_canvas"),
			myOptions);

	if (!initialLocation) {
		
		// Try W3C Geolocation (Preferred)
		if (navigator.geolocation) {
			browserSupportFlag = true;
			navigator.geolocation.getCurrentPosition(function(position) {
				currentLocation = new google.maps.LatLng(
						position.coords.latitude, position.coords.longitude);
				map.setCenter(currentLocation);
				initializeUserLocationPushpin();
			}, function() {
				handleNoGeolocation(browserSupportFlag);
			});
			// Try Google Gears Geolocation
		} else if (google.gears) {
			browserSupportFlag = true;
			var geo = google.gears.factory.create('beta.geolocation');
			geo.getCurrentPosition(function(position) {
				currentLocation = new google.maps.LatLng(position.latitude,
						position.longitude);
				map.setCenter(currentLocation);
				initializeUserLocationPushpin();
			}, function() {
				handleNoGeoLocation(browserSupportFlag);
			});
			// Browser doesn't support Geolocation
		} else {
			browserSupportFlag = false;
			handleNoGeolocation(browserSupportFlag);
		}
	} else {
		
	}

	function handleNoGeolocation(errorFlag) {
		if (errorFlag == true) {
			alert("Geolocation service failed.");
			currentLocation = clujNapoca;
		} else {
			alert("Your browser doesn't support geolocation. We've placed you in Siberia.");
			currentLocation = clujNapoca;
		}
		map.setCenter(currentLocation);
		initializeUserLocationPushpin();
	}
	
	function initializeUserLocationPushpin() {
		userLocationPushpin = new google.maps.Marker({
		    map: map,
		    position: currentLocation,
		    draggable: true
		});
	}
}