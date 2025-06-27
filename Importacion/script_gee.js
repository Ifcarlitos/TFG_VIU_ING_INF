// Función para enmascarar nubes
function maskS2clouds(image) {
  var qa = image.select('QA60');
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
               .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
  return image.updateMask(mask).divide(10000);
}

// EUCROPMAP 2018
var cropmap = ee.ImageCollection('JRC/D5/EUCROPMAP/V1')
  .filterDate('2018-01-01', '2019-01-01')
  .first();

// Fechas Sentinel-2 (julio 2020)
var startDate = '2020-07-01';
var endDate = '2020-07-31';

// Región: Terrassa (10 km x 10 km aprox)
var baseRegion = ee.Geometry.Rectangle([1.95, 41.53, 2.05, 41.63]);

// Dividir en 5x5 celdas
var rows = 5;
var cols = 5;
var deltaLon = (2.05 - 1.95) / cols;
var deltaLat = (41.63 - 41.53) / rows;

// Exportar cada celda
for (var row = 0; row < rows; row++) {
  for (var col = 0; col < cols; col++) {

    var xmin = 1.95 + col * deltaLon;
    var xmax = xmin + deltaLon;
    var ymin = 41.53 + row * deltaLat;
    var ymax = ymin + deltaLat;

    var cell = ee.Geometry.Rectangle([xmin, ymin, xmax, ymax]);
    var id = 'Terrassa_R' + row + '_C' + col;

    var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
      .filterDate(startDate, endDate)
      .filterBounds(cell)
      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
      .map(maskS2clouds)
      .median()
      .select(['B4', 'B3', 'B2'])
      .multiply(10000).toInt16();

    var crop = cropmap.clip(cell).rename('crop').toInt16();
    var combined = s2.addBands(crop);

    Export.image.toDrive({
      image: combined,
      description: id + '_S2_Crop',
      folder: 'tfg_viu',
      fileNamePrefix: id + '_2020',
      region: cell,
      scale: 10,
      maxPixels: 1e13,
      fileFormat: 'GeoTIFF'
    });
  }
}

// https://code.earthengine.google.com/