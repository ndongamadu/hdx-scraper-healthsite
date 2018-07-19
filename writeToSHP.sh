cd data
mkdir shapefiles
ogr2ogr -nlt POINT -skipfailures shapefiles/healthsites.shp healthsites.geojson
zip -r shapefiles.zip shapefiles/
rm -r shapefiles
