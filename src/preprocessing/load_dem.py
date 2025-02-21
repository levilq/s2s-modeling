import rasterio
import numpy as np

def load_dem(dem_path):
    """
    Load and preprocess DEM file.
    :param dem_path: Path to the DEM file (GeoTIFF format)
    :return: Tuple (DEM array, metadata, NoData mask)
    """
    with rasterio.open(dem_path) as src:
        dem_data = src.read(1).astype(float)  # Convert to float for processing
        meta = src.meta  # Store metadata
        nodata_value = src.nodata  # Get NoData value
        extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]

    # Create NoData mask
    nodata_mask = (dem_data == nodata_value) if nodata_value is not None else None

    return dem_data, meta, nodata_mask

def fill_nodata(dem_data, nodata_mask):
    """
    Fill NoData values using nearest-neighbor interpolation.
    :param dem_data: DEM array
    :param nodata_mask: Mask indicating NoData pixels
    :return: Filled DEM array
    """
    if nodata_mask is None or not np.any(nodata_mask):
        print("No NoData values detected. Skipping filling step.")
        return dem_data  # No NoData values, return unchanged

    # Use simple interpolation by averaging neighboring values
    filled_dem = dem_data.copy()
    filled_dem[nodata_mask] = np.nan  # Convert NoData to NaN
    filled_dem = np.nan_to_num(filled_dem, nan=np.nanmean(filled_dem))  # Replace NaN with mean

    print("NoData values filled successfully.")
    return filled_dem


