import rasterio
from rasterio.enums import Resampling

file1 = "C:/Users/loiq.amonbekov/PycharmProjects/s2s-modeling/data/raw/SarezWaterShed.tif"
with rasterio.open(file1) as src:
    pixel_size_x, pixel_size_y = src.res  # Get pixel size (resolution)
    print(f"Pixel Size of Reference Raster: {pixel_size_x}, {pixel_size_y}")


file2 = "C:/Users/loiq.amonbekov/PycharmProjects/s2s-modeling/data/raw/precip_annual_avg_33yr.tif"  # The file you want to downsample
output_file = "C:/Users/loiq.amonbekov/PycharmProjects/s2s-modeling/data/raw/precip_annual_avg_33yr_resampled.tif"  # Output file

with rasterio.open(file1) as ref:
    ref_pixel_size_x, ref_pixel_size_y = ref.res  # Get target pixel size

with rasterio.open(file2) as src:
    scale_x = src.res[0] / ref_pixel_size_x  # Compute scale factor
    scale_y = src.res[1] / ref_pixel_size_y

    new_width = int(src.width * scale_x)
    new_height = int(src.height * scale_y)

    # Resample data
    data = src.read(
        out_shape=(src.count, new_height, new_width),
        resampling=Resampling.bilinear  # You can use different methods
    )

    # Adjust the transform for the new resolution
    new_transform = src.transform * src.transform.scale(
        (src.width / new_width),
        (src.height / new_height)
    )

    # Save the resampled raster
    with rasterio.open(output_file, "w",
                       driver="GTiff",
                       height=new_height,
                       width=new_width,
                       count=src.count,
                       dtype=src.dtypes[0],
                       crs=src.crs,
                       transform=new_transform) as dst:
        dst.write(data)

print(f"Resampled raster saved as {output_file}")


with rasterio.open(output_file) as resampled:
    print(f"New Pixel Size: {resampled.res}")
