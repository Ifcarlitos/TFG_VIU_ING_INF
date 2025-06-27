from anyio import sleep
import ee

# ee.Authenticate()  # Autenticación de Earth Engine

ee.Initialize(project='yoloshipcromerom')

# 1. Definir región AMB (Área Metropolitana de Barcelona)
xmin, ymin = 1.95, 41.25  # Aprox. Llobregat inferior
xmax, ymax = 2.45, 41.65  # Aprox. Badalona / Montcada
rows, cols = 10, 10

delta_lon = (xmax - xmin) / cols
delta_lat = (ymax - ymin) / rows

# 2. Años a procesar
years = [2020, 2022, 2024]

# 3. Capa de referencia EUCROPMAP (aunque sea de 2018, se reutiliza para todas)
cropmap = ee.ImageCollection('JRC/D5/EUCROPMAP/V1') \
    .filterDate('2018-01-01', '2019-01-01') \
    .first()

# 4. Máscara de nubes Sentinel-2
def maskS2clouds(image):
    qa = image.select('QA60')
    cloud_bit = 1 << 10
    cirrus_bit = 1 << 11
    mask = qa.bitwiseAnd(cloud_bit).eq(0).And(qa.bitwiseAnd(cirrus_bit).eq(0))
    return image.updateMask(mask).divide(10000)

# 5. Loop para exportar imágenes por celda y año
for year in years:
    start_date = f'{year}-01-01'
    end_date = f'{year}-12-31'

    for row in range(rows):
        for col in range(cols):
            cell_xmin = xmin + col * delta_lon
            cell_xmax = cell_xmin + delta_lon
            cell_ymin = ymin + row * delta_lat
            cell_ymax = cell_ymin + delta_lat

            region = ee.Geometry.Rectangle([cell_xmin, cell_ymin, cell_xmax, cell_ymax])
            cell_id = f"AMB_R{row}_C{col}"
            bandas_s2 = ['B4', 'B3', 'B2', 'QA60']  # Red, Green, Blue + máscara nubes

            s2_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
                .filterDate(start_date, end_date) \
                .filterBounds(region) \
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
                .select(bandas_s2) \
                .map(maskS2clouds)

            if s2_collection.size().getInfo() == 0:
                print(f"Sin imágenes para {cell_id} en {year}.")
                continue

            s2 = s2_collection.median().select(['B4', 'B3', 'B2']).multiply(10000).toInt16()
            crop = cropmap.clip(region).rename('crop').toInt16()
            combined = s2.addBands(crop)

            task = ee.batch.Export.image.toDrive(
                image=combined,
                description=f"{cell_id}_S2_Crop_{year}",
                folder='TFG_GEE_AMB_Exports_'+ str(year),
                fileNamePrefix=f"{cell_id}_{year}",
                region=region.getInfo()['coordinates'],
                scale=10,
                maxPixels=1e13,
                fileFormat='GeoTIFF'
            )

            task.start()
            print(f"Tarea lanzada: {cell_id}_{year}")