
function initialize_your_location(latitude, longitude, pushpinPath, postbackLink, isEvent) {
	
	var initialLocation = null;
	
	if (latitude != null && longitude != null) {
		initialLocation = new google.maps.LatLng(latitude, longitude);
	}
	
	var clujNapoca = new google.maps.LatLng(46.7667, 23.6);
	
	if (isEvent) {
		initialLocation = clujNapoca;
	}
	
	var browserSupportFlag = new Boolean();
	var map = null;
	var userLocationPushpin = null;
	
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
				initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
				initializeUserLocationPushpin();
				map.setCenter(initialLocation);
			}, function() {
				handleNoGeolocation(browserSupportFlag);
			});
			// Try Google Gears Geolocation
		} else if (google.gears) {
			browserSupportFlag = true;
			var geo = google.gears.factory.create('beta.geolocation');
			geo.getCurrentPosition(function(position) {
				initialLocation = new google.maps.LatLng(position.latitude, position.longitude);
				initializeUserLocationPushpin();
				map.setCenter(initialLocation);
			}, function() {
				handleNoGeoLocation(browserSupportFlag);
			});
			// Browser doesn't support Geolocation
		} else {
			browserSupportFlag = false;
			handleNoGeolocation(browserSupportFlag);
		}
	} else {
		initializeUserLocationPushpin();
		map.setCenter(initialLocation);
	}
	
	function handleNoGeolocation(errorFlag) {
		if (errorFlag == true) {
			alert("Geolocation service failed.");
			initialLocation = clujNapoca;
		} else {
			alert("Your browser doesn't support geolocation. We've placed you in Cluj-Napoca.");
			initialLocation = clujNapoca;
		}
		map.setCenter(initialLocation);
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
		    position: initialLocation,
		    draggable: true,
		    shadow: shadow,
		    shape: shape,
		    icon: image
		});
	}
			
	function postUserLatLng(latitude, longitude) {
		var requestData = { 'lat': latitude , 'lng': longitude };
		
		$.ajax({
			data: JSON.stringify(requestData),
		    processData: false,
		    contentType: 'application/json',			
		    type: "POST",
		    url: postbackLink,
		    success: function(data){
		    	alert(data);
		    },
		    error: function(msg){
		    	alert("There was an error with the server." );
		    }              
		});
	}
	
	function postEventLatLng(latitude, longitude) {
		var requestData = { 'lat': latitude , 'lng': longitude };
		
		$.ajax({
			data: JSON.stringify(requestData),
		    processData: false,
		    contentType: 'application/json',			
		    type: "POST",
		    url: postbackLink,
		    success: function(data){
		    	window.location.href = data;
		    },
		    error: function(msg){
		    	alert("There was an error with the server." );
		    }              
		});
	}
	
	function leave_locations(e) {
		if (!isEvent &&
			(initialLocation == null || 
			userLocationPushpin.getPosition().lng() != initialLocation.lng() || 
			userLocationPushpin.getPosition().lat() != initialLocation.lat())) {
			
			return 'You have changed your current location, but it is not yet saved to the database.';
		}
	}	
	
	var controlsHolder = document.createElement('DIV');
	controlsHolder.style.padding = '30px';
	controlsHolder.style.paddingTop = '10px';
	controlsHolder.style.paddingBottom = '10px';
	controlsHolder.style.border = '3px solid #fff';
	controlsHolder.style.backgroundColor = '#ac74e3';
	controlsHolder.index = 1;
	


    var saveLocationControl = document.createElement('DIV');
	saveLocationControl.style.padding = '3px';
	saveLocationControl.style.paddingLeft = '10px';
	saveLocationControl.style.paddingRight = '10px';
	saveLocationControl.style.border = '1px solid #003399';
	saveLocationControl.style.backgroundColor = '#fff';
	saveLocationControl.style.cursor = 'pointer';
	saveLocationControl.innerHTML = '<b>Save location</b>';
	
	controlsHolder.appendChild(saveLocationControl);
	
	google.maps.event.addDomListener(saveLocationControl, 'click', function() {
		if (isEvent) {
			postEventLatLng(userLocationPushpin.getPosition().lat(), userLocationPushpin.getPosition().lng());
		} else {
			postUserLatLng(userLocationPushpin.getPosition().lat(), userLocationPushpin.getPosition().lng());
			initialLocation = new google.maps.LatLng(userLocationPushpin.getPosition().lat(), userLocationPushpin.getPosition().lng());
		}
	});
	
	map.controls[google.maps.ControlPosition.TOP].push(controlsHolder);
	window.onbeforeunload = leave_locations;
}
