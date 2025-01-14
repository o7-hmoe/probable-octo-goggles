import numpy as np
import os
from osgeo import ogr
from osgeo import gdal

def raster2array(raster_file_name):
    """
    Converts a raster file to a numpy array and retrieves geo-transform information.

    :param raster_file_name: STR path to the raster file.
    :return: A tuple containing:
        - raster (osgeo.gdal.Dataset): The GDAL raster dataset.
        - array (numpy.ndarray): The raster data as a numpy array.
        - geo_transform (tuple): The geo-transform information of the raster.
    """
    # Open the raster file
    raster = gdal.Open(raster_file_name)
    if not raster:
        raise FileNotFoundError(f"Cannot open raster file: {raster_file_name}")

    # Get the first band (assuming single-band raster)
    band = raster.GetRasterBand(1)
    if not band:
        raise ValueError(f"Cannot access raster band in file: {raster_file_name}")

    # Read the raster data into a numpy array
    array = band.ReadAsArray()

    # Get geo-transform information (required for spatial referencing)
    geo_transform = raster.GetGeoTransform()

    # Return the raster dataset, array, and geo-transform
    return raster, array, geo_transform

def create_shp(shp_file_dir, overwrite=True, **kwargs):
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

def offset2coords(geo_transform, offset_x, offset_y):
    # get origin and pixel dimensions from geo_transform (osgeo.gdal.Dataset.GetGeoTransform() object)
    origin_x = geo_transform[0]
    origin_y = geo_transform[3]
    pixel_width = geo_transform[1]
    pixel_height = geo_transform[5]

    # calculate x and y coordinates
    coord_x = origin_x + pixel_width * (offset_x + 0.5)
    coord_y = origin_y + pixel_height * (offset_y + 0.5)

    # return x and y coordinates
    return coord_x, coord_y

def raster2line(raster_file_name, out_shp_fn, pixel_value):
    # Extract raster data
    raster, array, geo_transform = raster2array(raster_file_name)

    # Extract pixel positions with the given pixel_value
    trajectory = np.where(array == pixel_value)
    if np.count_nonzero(trajectory) == 0:
        print(f"ERROR: The defined pixel_value ({pixel_value}) does not occur in the raster band.")
        return None

    # Collect the center coordinates of each pixel, scanning left to right
    points = []
    for x in range(array.shape[1]):  # Scan columns (left to right)
        for y in range(array.shape[0]):  # Scan rows within each column
            if array[y, x] == pixel_value:
                x_center, y_center = offset2coords(geo_transform, x, y)
                points.append((x_center, y_center))

    # Create the line geometry
    line = ogr.Geometry(ogr.wkbLineString)
    for point in points:
        line.AddPoint(point[0], point[1])

    # Write the line geometry to a shapefile
    new_shp = create_shp(out_shp_fn, layer_name="raster_line", layer_type="line")
    lyr = new_shp.GetLayer()
    feature_def = lyr.GetLayerDefn()
    new_line_feat = ogr.Feature(feature_def)
    new_line_feat.SetGeometry(line)
    lyr.CreateFeature(new_line_feat)
    print(f"Success: Wrote {out_shp_fn}")


gdal.UseExceptions()
source_raster_fn = r"" +  os.path.abspath("") + "/least-cost.tif"
target_shp_fn = r"" + os.path.abspath("") + "/least-cost.shp"
pixel_val = 1
raster2line(source_raster_fn, target_shp_fn, pixel_val)
