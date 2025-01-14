from osgeo import osr
from osgeo import ogr
import os

station_names = {"Plochingen": (1048277.00, 6225451.07),
                 "Esslingen": (1035877.89, 6231142.47),
                 "Bad Cannstatt": (1025264.60, 6241160.48),
                 "Muhlhausen": (1029184.69, 6249000.67),
                 "Remseck": (1032095.73, 6253407.14),
                 "Neckbiotop": (1030582.63, 6259483.23),
                 "Neckarweihingen": (1026302.70, 6259599.44),
                 "Marbach": (1029954.19, 6264869.79)}

def create_shp(shp_file_dir, overwrite=True, *args, **kwargs):
    shp_driver = ogr.GetDriverByName("ESRI Shapefile")

    if os.path.exists(shp_file_dir) and overwrite:
        shp_driver.DeleteDataSource(shp_file_dir)

    new_shp = shp_driver.CreateDataSource(shp_file_dir)

    if kwargs.get("layer_name") and kwargs.get("layer_type"):
        geometry_dict = {"point": ogr.wkbPoint,
                         "line": ogr.wkbMultiLineString,
                         "polygon": ogr.wkbMultiPolygon}
        try:
            new_shp.CreateLayer(str(kwargs.get("layer_name")),
                                geom_type=geometry_dict[str(kwargs.get("layer_type").lower())])
        except KeyError:
            print("Error: Invalid layer_type provided (must be 'point', 'line', or 'polygon').")
        except TypeError:
            print("Error: layer_name and layer_type must be strings.")
        except AttributeError:
            print("Error: Cannot access layer. Is the file open in another program?")
    return new_shp


def get_wkt(epsg, wkt_format="esriwkt"):
    default = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],' \
              'PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295],UNIT["Meter",1]]'
    spatial_ref = osr.SpatialReference()
    try:
        spatial_ref.ImportFromEPSG(epsg)
    except TypeError:
        print("ERROR: EPSG must be an integer. Returning default WKT (EPSG=4326).")
        return default
    except Exception:
        print("ERROR: EPSG number does not exist. Returning default WKT (EPSG=4326).")
        return default
    if wkt_format == "esriwkt":
        spatial_ref.MorphToESRI()
    return spatial_ref.ExportToPrettyWkt()

#prevent OSR warning message
osr.UseExceptions()

# Main script
shp_dir = os.path.join(os.path.abspath(""), "neckar_approx.shp")
rhine_line = create_shp(shp_dir, layer_name="basemap", layer_type="line")

with open(shp_dir.replace(".shp", ".prj"), "w") as prj:
    prj.write(get_wkt(3857))

lyr = rhine_line.GetLayer()



line = ogr.Geometry(ogr.wkbLineString)
for stn in station_names.values():
    line.AddPoint(stn[0], stn[1])

field_name = ogr.FieldDefn("river", ogr.OFTString)
lyr.CreateField(field_name)

line_feature = ogr.Feature(lyr.GetLayerDefn())
line_feature.SetGeometry(line)
line_feature.SetField("river", "Rhine")
lyr.CreateFeature(line_feature)

# prevent memory leaks
line.Destroy()
line_feature.Destroy()

lyr = None
rhine_line = None