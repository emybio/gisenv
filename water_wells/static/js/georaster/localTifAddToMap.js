



// initalize leaflet map
var map = L.map('map').setView([36.844829, 34.679856], 10);

var marker;



// add OpenStreetMap basemap
var wi = L.tileLayer('http://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    opacity: 1,
    zoomControl: false,
});

var wsm = L.tileLayer('http://services.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
    opacity: 1,
    zoomControl: false,
    attribution: '&copy; CartoDB'
});


var osm = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    opacity: 1,
    zoomControl: false,

});

wsm.addTo(map);
var baseMaps = {

    "World Street Map": wsm,
    "World Imagery": wi,
    "OSM Mapnik": osm

};

/*
  // Bounds of the image
  var imageUrl = '{% static "maps/png/ekran.png" %}';
  var imageBounds = [[40.712, -74.227], [40.774, -74.125]];  // Adjust coordinates

  var defeUrl = '{% static "maps/png/defe.png" %}';
  var defeBounds = [[36.5, 34.0],  // Sol üst köşe koordinatları
  [36.375, 34.125]  // Sağ alt köşe koordinatları
  ];


  var p31url = '{% static "maps/jpg/p31.jpg" %}';
  var p31Bounds = [[36.5, 34.0],  // Sol üst köşe koordinatları
  [34.00, 36.50]  // Sağ alt köşe koordinatları
  ];

  var p32a1 = '{% static "maps-jpg/p32a1.img" %}'

  // Image overlay1
  var ornekMap = L.imageOverlay(imageUrl, imageBounds, { opacity: 1, });

  // Image overlay2
  var defeMap = L.imageOverlay(defeUrl, defeBounds, { opacity: 1 });

  var p31Map = L.imageOverlay(p31url, p31Bounds, { opacity: 1 })

  var p32a1Map = L.imageOverlay(p32a1, null);

  // Adjust center and zoom level to fit the image
  //map.fitBounds(imageBounds);
  //map.fitBounds(defeMap);

  ornekLayer = { "ornek": ornekMap, "Silifke P32A1": defeMap, "Silifke P31": p31Map, "P32A1": p32a1Map };
*/
L.control.layers(baseMaps, tifLayer).addTo(map);



// Sidebar oluşturun
let sidebarControl = L.control.sidebar('sidebar', {
    position: 'left'
}).addTo(map);




// Adjust Sidebar Height
function adjustSidebarHeight() {
    setTimeout(() => {
        let sidebarElement = document.getElementById('sidebar');
        let content = sidebarElement.querySelector('.leaflet-sidebar-content');


        sidebarElement.style.height = 'auto';// Varsayılan yüksekliği sıfırla
        content.style.height = 'auto'; // Varsayılan yüksekliği sıfırla



        let addedHeight = content.scrollHeight + 5;
        sidebarElement.style.height = content.scrollHeight + 'px';

    }, 0);


}

window.addEventListener('load', function () {
    adjustSidebarHeight();
});

window.addEventListener('resize', function () {
    adjustSidebarHeight();
});

sidebarControl.on('content', function () {
    adjustSidebarHeight();
});


// Katman eklendiğinde zoom yapın ve slider'ı ayarlayın
let currentLayer = null;
map.on('overlayadd', function (e) {
    currentLayer = e.layer;
    let bounds = e.layer.getBounds();
    map.fitBounds(bounds);


    let opacitySlider = document.getElementById('opacitySlider');

    // Slider olayını ayarla
    opacitySlider.oninput = opacitySlider.onchange = function () {
        currentLayer.setOpacity(this.value);
    };
});

// Slider başlangıç değeri
document.getElementById('opacitySlider').value = 1;

// Katman kaldırıldığında slider'ı sıfırla
map.on('overlayremove', function (e) {
    document.getElementById('opacitySlider').oninput = null;
    currentLayer = null;
});

// Sidebar'ı açmak için bir olay ekleyin
document.querySelector('a[href="#opacity"]').addEventListener('click', function () {
    sidebarControl.open('opacity');
});
let activeTab = null;
document.querySelectorAll('.leaflet-sidebar-tabs ul li a').forEach(tab => {
    tab.addEventListener('click', function () {
        if (activeTab === this) {
            sidebarControl.close();
            activeTab = null;
        } else {
            sidebarControl.open(this.getAttribute('href').substring(1));
            activeTab = this;
        }
    });
});










//Form Bilgileri ile Kaydetme
document.getElementById('coordinate-form').addEventListener('submit', function (event) {
    event.preventDefault();

    var formData = new FormData(this);

    fetch('/add_location/', {
        method: 'POST',
        body: new URLSearchParams(formData),
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    }).then(response => response.json())
        .then(data => {
            if (data.status === 'success') {

                alert('Location saved!' + " - " + data);
                //location.reload();
            } else {
                alert('Failed to save location');
                console.log(data.errors); // Hata mesajlarını konsola yazdır
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});


// Modal control
var modal = document.getElementById("infoModal");
var span = document.getElementsByClassName("close")[0];
var removeBtn = document.getElementById("removeBtn");




function addMarker(f) {


    map.on('click', function (e) {

        var bilgi = document.getElementById("info").value;
        var latlng = e.latlng;

        // Transform coordinates from WGS84 to ED50
        //EPSG European Petroleum Survey Group (Avrupa Petrol Ölçme Grubu) 4326 WGS84'e karşılık gelmektedir.
        //şimdilik 4326'yı 23036 yaptım denemek için.
        var latlonED50 = proj4("EPSG:4326", ed50, [latlng.lng, latlng.lat]);
        //proj4('EPSG:23036', ed50, [latlng.lng, latlng.lat]);

        // Transform coordinates from ED50 to UTM
        var utmCoords = proj4(ed50, utm36n, latlonED50);

        marker = L.marker([latlng.lat, latlng.lng]).bindTooltip(bilgi).addTo(map);


        document.getElementById("lat").value = utmCoords[1];
        document.getElementById("lon").value = utmCoords[0];
        modal.style.display = "block";




    });

    span.onclick = function () {
        modal.style.display = "none";
        console.log("span tıklandı : ",marker);
        map.removeLayer(marker)
    }



    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
            console.log("window tıklandı : ",marker);
            map.removeLayer(marker)

        }
    }


}







// Handle the radio buttons for selecting the drawing mode
document.querySelectorAll('.radioBtn').forEach(radio => {
    radio.addEventListener('change', function () {
        if (this.value === 'marker') {
            // Disable polygon drawing and enable marker adding

            map.on('click', addMarker);

            console.log("marker işaretli")

        } else if (this.value === 'polygon') {
            // Enable polygon drawing and disable marker adding
            //map.off('click', addMarker);
            console.log("polygon işaretli")
            
        }
    });
});
map.on('draw:created', function (e) {
    var coords = e.layer._latlng;
    console.log(coords);
    var tempMarker = featureGroup.addLayer(e.layer);
    var popupContent = '<form role="form" id="form" enctype="multipart/form-data" class = "form-horizontal" onsubmit="addMarker()">' +
        '<div class="form-group">' +
        '<label class="control-label col-sm-5"><strong>Date: </strong></label>' +
        '<input type="date" placeholder="Required" id="date" name="date" class="form-control"/>' +
        '</div>' +
        '<div class="form-group">' +
        '<label class="control-label col-sm-5"><strong>Gender: </strong></label>' +
        '<select class="form-control" id="gender" name="gender">' +
        '<option value="Male">Male</option>' +
        '<option value="Female">Female</option>' +
        '<option value="Other">Other</option>' +
        '</select>' +
        '</div>' +
        '<div class="form-group">' +
        '<label class="control-label col-sm-5"><strong>Age: </strong></label>' +
        '<input type="number" min="0" class="form-control" id="age" name="age">' +
        '</div>' +
        //...
        '<div class="form-group">' +
        '<label class="control-label col-sm-5"><strong>Description: </strong></label>' +
        '<textarea class="form-control" rows="6" id="descrip" name="descript">...</textarea>' +
        '</div>' +
        '<input style="display: none;" type="text" id="lat" name="lat" value="' + coords.lat.toFixed(6) + '" />' +
        '<input style="display: none;" type="text" id="lng" name="lng" value="' + coords.lng.toFixed(6) + '" />' +
        '<div class="form-group">' +
        '<div style="text-align:center;" class="col-xs-4 col-xs-offset-2"><button type="button" class="btn">Cancel</button></div>' +
        '<div style="text-align:center;" class="col-xs-4"><button type="submit" value="submit" class="btn btn-primary trigger-submit">Submit</button></div>' +
        '</div>' +
        '</form>';
    tempMarker.bindPopup(popupContent, {
        keepInView: true,
        closeButton: false
    }).openPopup();

    $("#form").submit(function (e) {
        e.preventDefault();
        console.log("didnt submit");
        var date = $("#date").val();
        console.log(date);

    });
});








function saveInfo() {
    var lat = document.getElementById("lat").value;
    var lon = document.getElementById("lon").value;
    var info = document.getElementById("info").value;

    var formData = new FormData();
    formData.append('lat', lat);
    formData.append('lon', lon);
    formData.append('info', info);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');



    fetch('/add_location/', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Location saved!');
                //location.reload();
            } else {
                alert('Failed to save location');
            }
            modal.style.display = "none";
        })
        .catch(error => console.error('Error:', error));
}



// Function to load and display UTM coordinates from the database
// function loadUTMPoints() {
//   fetch('/get_locations/')
//     .then(response => response.json())
//     .then(data => {
//       data.locations.forEach(location => {
//         var utmCoords = [location.lon, location.lat];
//         var wgs84Coords = proj4(utm33n, wgs84, utmCoords);
//         L.marker([wgs84Coords[1], wgs84Coords[0]]).addTo(map)
//           .bindPopup(`Info: ${location.info}`);
//       });
//     })
//     .catch(error => console.error('Error:', error));
// }

// Load UTM points when the map is ready
// map.on('load', loadUTMPoints);
// map.fire('load');


// document.getElementById('shapefile-input').addEventListener('change', function (event) {
//   var files = event.target.files;
//   if (files.length) {
//     var shpFile = null, dbfFile = null;

//     for (var i = 0; i < files.length; i++) {
//       if (files[i].name.endsWith('.shp')) {
//         shpFile = files[i];
//       } else if (files[i].name.endsWith('.dbf')) {
//         dbfFile = files[i];
//       }
//     }

//     if (shpFile && dbfFile) {
//       var reader = new FileReader();
//       reader.onload = function (e) {
//         var shpBuffer = e.target.result;
//         var dbfReader = new FileReader();
//         dbfReader.onload = function (e) {
//           var dbfBuffer = e.target.result;
//           shp.parseShp(shpBuffer, shp.parseDbf(dbfBuffer)).then(function (geojson) {
//             L.geoJSON(geojson).addTo(map);
//           }).catch(error => console.error(error));
//         };
//         dbfReader.readAsArrayBuffer(dbfFile);
//       };
//       reader.readAsArrayBuffer(shpFile);
//     } else {
//       alert('Please select both .shp and .dbf files.');
//     }
//   }
// });



/***************************************************************************************************/
// input:file  ile dosya yükleyerek tif görüntülemek istediğimizde kullanacağımız kodlar:

// var tifLayer;
// document.getElementById("geotiff-file").addEventListener("change", function (event) {
//   var file = event.target.files[0];

//   console.log("file:", file);

//   var reader = new FileReader();
//   reader.readAsArrayBuffer(file);
//   reader.onloadend = function () {
//     var arrayBuffer = reader.result;
//     parseGeoraster(arrayBuffer).then(georaster => {

//       console.log("georaster:", georaster);
/*
    GeoRasterLayer is an extension of GridLayer,
    which means can use GridLayer options like opacity.

    Just make sure to include the georaster option!

    http://leafletjs.com/reference-1.2.0.html#gridlayer
*/


//       tifLayer = new GeoRasterLayer({
//         georaster: georaster,
//         opacity: 0.9,
//         resolution: 200,
//       });
//       console.log("layer:", tifLayer);
//       tifLayer.addTo(map);
//       map.fitBounds(tifLayer.getBounds());


//  document.getElementById("overlay").style.display = "none";
//     });
//   };
// });





var opacity;

document.getElementById('opacitySlider').addEventListener('input', function () {
    opacity = this.value;
    Object.values(layers).forEach(layer => {
        layer.setOpacity(opacity);
    });
});



// TIFF dosyalarını listeleme
var layers = {}; // Katmanları saklamak için bir nesne
// TIFF dosyalarını listeleme ve yükleme

var tifLayer;
fetch('./api/layers')
    .then(response => response.json())
    .then(layersList => {
        var layerControls = document.getElementById('layer-list');
        layersList.forEach(layer => {
            var checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = layer.name;
            checkbox.dataset.url = layer.url;
            checkbox.dataset.name = layer.name;
            checkbox.addEventListener('change', function () {
                handleLayerChange(this);
            });

            var label = document.createElement('label');
            label.htmlFor = layer.name;
            label.textContent = layer.name;

            var div = document.createElement('div');
            div.appendChild(checkbox);
            div.appendChild(label);
            layerControls.appendChild(div);

            //console.log(`Checkbox created: ${layer.name} with URL ${layer.url}`);
        });
    })
    .catch(error => console.error('Error fetching layer list:', error));

function handleLayerChange(checkbox) {
    var url = checkbox.dataset.url;
    var layerName = checkbox.dataset.name;

    if (!layerName) {
        console.error('Layer name is not defined.');
        return;
    }

    //  console.log(`Handling layer change for: ${layerName}, checked: ${checkbox.checked}`);
    // TIFF katmanının pane'yi doğru şekilde ayarlayın
    map.createPane('tifPane');
    map.getPane('tifPane').style.zIndex = 1000; // TIFF katmanının yüksek z-index değeri
    if (checkbox.checked) {
        fetch(url)
            .then(response => response.arrayBuffer())
            .then(arrayBuffer => parseGeoraster(arrayBuffer))
            .then(georaster => {
                tifLayer = new GeoRasterLayer({
                    georaster: georaster,
                    opacity: opacity,
                    resolution: 256,
                    pane: 'tifPane',
                    async: true // Performans artırımı için async olarak ayarla

                });
                tifLayer.addTo(map);
                layers[layerName] = tifLayer; // Katmanı sakla
                map.fitBounds(tifLayer.getBounds());
                tifLayer.addTo(map);

            })
            .catch(error => console.error('Error loading TIFF layer:', error));
    } else {
        var tifLayer = layers[layerName];
        if (tifLayer) {
            map.removeLayer(tifLayer);
            delete layers[layerName]; // Katmanı saklanan nesneden kaldır
            // console.log('Layer removed:', layerName);
        } else {
            console.log('No layer to remove for:', layerName);
        }
    }
}


function parseGeoraster(arrayBuffer) {
    return GeoRaster(arrayBuffer);
}

// TIFF katmanını en son ekleyin
map.eachLayer(function (layer) {
    if (layer instanceof GeoRasterLayer) {
        map.removeLayer(layer);
        setTimeout(function () {
            map.addLayer(layer);
        }, 0); // Katmanı hemen eklemek için küçük bir gecikme
    }
});



// Harita değiştirilince TIFF katmanını yeniden ekle
map.on('baselayerchange', function (eventLayer) {
    if (tifLayer) {
        map.removeLayer(tifLayer); // Önceki TIFF katmanını kaldır
        tifLayer.addTo(map); // TIFF katmanını yeniden ekle
        tifLayer.bringToFront(); // TIFF katmanını üstte tutmak için
    }
});


//chooseAction();


