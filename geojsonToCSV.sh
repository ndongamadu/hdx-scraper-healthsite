cd data
ogr2ogr -skipfailures -f "CSV" healthsites.csv -lco GEOMETRY=AS_XY healthsites.geojson
