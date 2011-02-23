from django import forms
from django.db import models
from django.utils.safestring import mark_safe

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 700

DEFAULT_LAT = 46.7667
DEFAULT_LNG = 23.6

class MapTypes:
    USER_LOCATION=1
    EVENT_LOCATION=2
    USER_DISPLAY=3
    EVENT_DISPLAY=4

class LocationWidget(forms.TextInput):
    def __init__(self, *args, **kw):

        self.map_width = kw.get("map_width", DEFAULT_WIDTH)
        self.map_height = kw.get("map_height", DEFAULT_HEIGHT)
        self.map_type = kw.get("map_type", MapTypes.USER_LOCATION)
        self.pushpin_path = kw.get("pushpin_path", "/site_media/media/pushpins/root.png")
                                   
        super(LocationWidget, self).__init__(*args, **kw)
        self.inner_widget = forms.widgets.HiddenInput()

    def render(self, name, value, *args, **kwargs):
        if value is None:
            lat, lng = DEFAULT_LAT, DEFAULT_LNG
        else:
            if isinstance(value, unicode):
                a, b = value.split(',')
            else:
                a, b = value
            lat, lng = float(a), float(b)

        js = '''
            <script src="http://maps.google.com/maps/api/js?sensor=false" type="text/javascript"></script>s         var input = document.getElementById("id_%(name)s");
                    input.value = point.lat().toFixed(6) + "," + point.lng().toFixed(6);
                    map_%(name)s.panTo(point);
                }
                
                function submitForm() {
                    document.mapform.submit();
                }
                
                function load_%(name)s() {
                    var point = new google.maps.LatLng(%(lat)f, %(lng)f);
            
                    var options = {
                        zoom: 13,
                        center: point,
                        mapTypeId: google.maps.MapTypeId.ROADMAP
                        // mapTypeControl: true,
                        // navigationControl: true
                    };
                    
                    map_%(name)s = new google.maps.Map(document.getElementById("map_%(name)s"), options);
            
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
            
                    var marker = new google.maps.Marker({
                            map: map_%(name)s,
                            position: new google.maps.LatLng(%(lat)f, %(lng)f),
                            draggable: true,
                            shadow: shadow,
                            shape: shape,
                            icon: image                    
                    });
                    
                    var control = document.createElement('DIV');
                    control.style.padding = '5px';
                    control.style.border = '1px solid #000';
                    control.style.backgroundColor = 'white';
                    control.style.cursor = 'pointer';
                    control.innerHTML = 'Save Location';
                    control.index = 1;

                    google.maps.event.addDomListener(control, 'click', function() {
                        submitForm();
                    });
                    map_%(name)s.controls[google.maps.ControlPosition.TOP_RIGHT].push(control);
                    
                    google.maps.event.addListener(marker, 'dragend', function(mouseEvent) {
                        savePosition_%(name)s(mouseEvent.latLng);
                    });
            
                    google.maps.event.addListener(map_%(name)s, 'click', function(mouseEvent){
                        marker.setPosition(mouseEvent.latLng);
                        savePosition_%(name)s(mouseEvent.latLng);
                    });
            
                }
                
                $(document).ready(function(){
                    load_%(name)s();
                });
            
            </script>
        ''' % dict(name=name, lat=lat, lng=lng, pushpinPath=self.pushpin_path)
        html = self.inner_widget.render("%s" % name, "%f,%f" % (lat, lng), dict(id='id_%s' % name))
        html += '<div id="map_%s" style="width: %dpx; height: %dpx"></div>' % (name, self.map_width, self.map_height)

        return mark_safe(js + html)

    #class Media:
    #    js = (
    #    )

class LocationFormField(forms.CharField):
    def clean(self, value):
        if isinstance(value, unicode):
            a, b = value.split(',')
        else:
            a, b = value

        lat, lng = float(a), float(b)
        return lat, lng

class LocationField(models.CharField):
    def formfield(self, **kwargs):
        defaults = {'form_class': LocationFormField}
        defaults['widget'] = LocationWidget
        defaults.update(kwargs)
        
        return super(LocationField, self).formfield(**defaults)

