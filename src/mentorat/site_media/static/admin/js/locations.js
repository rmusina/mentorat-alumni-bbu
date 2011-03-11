var initialLocation = null;
var currentLocation = null;
var clujNapoca = new google.maps.LatLng(46.7667, 23.6);
var browserSupportFlag = new Boolean();
var map = null;
var userLocationPushpin = null;
var pushpinPath = '';

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
		currentLocation = initialLocation;
		initializeUserLocationPushpin();
	}

	function handleNoGeolocation(errorFlag) {
		if (errorFlag == true) {
			alert("Geolocation service failed.");
			currentLocation = clujNapoca;
		} else {
			alert("Your browser doesn't support geolocation. We've placed you in Cluj-Napoca.");
			currentLocation = clujNapoca;
		}
		map.setCenter(currentLocation);
		initializeUserLocationPushpin();
	}
	
	function initializeUserLocationPushpin() {
		var image = new google.maps.MarkerImage(
			pushpinPath,
			new google.maps.Size(30, 39), new google.maps.Point(0, 0),
			new google.maps.Point(15, 39));
		
		var shadow = new google.maps.MarkerImage(
			'/site_media/media/pushpins/shadow.png',
			new google.maps.Size(54,39),
			new google.maps.Point(0,0),
			new google.maps.Point(15,39));

		var shape = {
			coord: [16,0,20,1,21,2,23,3,24,4,25,5,26,6,27,7,27,8,28,9,28,10,28,11,29,12,29,13,29,14,29,15,29,16,29,17,28,18,28,19,28,20,27,21,27,22,26,23,25,24,25,25,24,26,22,27,21,28,18,29,17,30,17,31,17,32,16,33,16,34,16,35,15,36,15,37,15,38,14,38,14,37,13,36,13,35,13,34,12,33,12,32,12,31,12,30,11,29,8,28,7,27,5,26,4,25,3,24,3,23,2,22,2,21,1,20,1,19,0,18,0,17,0,16,0,15,0,14,0,13,0,12,1,11,1,10,1,9,2,8,2,7,3,6,4,5,5,4,6,3,7,2,9,1,13,0,16,0],
			type: 'poly'};

		userLocationPushpin = new google.maps.Marker({
		    map: map,
		    position: currentLocation,
		    draggable: true,
		    shadow: shadow,
		    shape: shape,
		    icon: image
		});
	}
	
	function leave_locations(e) {
		if (initialLocation == null || 
			userLocationPushpin.getPosition().lng() != initialLocation.lng() || 
			userLocationPushpin.getPosition().lat() != initialLocation.lat()) {
			
			var saveLocation = confirm('Do you want to save your new location?');
			
			if (saveLocation) {
				alert(userLocationPushpin.getPosition().lat() + " "
						+ userLocationPushpin.getPosition().lng());
				
				var locationJSON = {
					lat : userLocationPushpin.getPosition().lat(),
					lng : userLocationPushpin.getPosition().lng()
				};
				
				if (jQuery) {  
				    alert("jQuery OK");
				} else {
					alert("jQuery caca");
				}
				
				$.post('/locations/your_location/', locationJSON, function(result) {
		            alert(result.Result);
		        })


			} else {
				alert('not saving');
			}
			
			initialLocation = null;
			currentLocation = null;
			userLocationPushpin = null;
		}
	}
	
	window.onbeforeunload=leave_locations;
}
