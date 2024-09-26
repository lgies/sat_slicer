# sat_slicer
slice satelitte images for analysis

# usage
```python slice_image.py --image_path "./images" --image_file_name "my_satellite_image.tif" --output_path "./tiles" --tile_size 512 512 --overlap 0.2

# parameters
Parameters:
``` --image_path: The directory where the satellite image is located. (Default: . which refers to the current directory).
--image_file_name: The name of the image file to be sliced. (Default: 'satellite_image.tif').
--output_path: The directory where the tiles will be saved. (Default: ./output_tiles).
--tile_size: The size of each tile in pixels. This should be provided as two integers (e.g., 256 256)(Default: 256x256).
--overlap: The overlap between tiles as a percentage. (Default: 0.1, or 10%).
```

# Key Points:

## Image Input:
The script uses rasterio to open geospatial satellite images and handles georeferencing information.

## Tile Size and Overlap:
The tile_size parameter defines the size of the sliced tiles (default is 256x256 pixels).
The overlap parameter specifies the percentage overlap between tiles (default is 10%).

## Naming Convention:
Each tile is named with a convention that includes the UTM zone, coordinates of the upper-left corner of the tile, the date and time of image acquisition, and the tile size.

## Output:
The tiles are saved in the specified output_dir in PNG format, with the georeferenced data stored in the filename.

## Example of Output File Naming:

```tile_UTM32_563400E_5432000N_20230924T103000_256x256.png

# Additional Notes:

The script extracts metadata such as image acquisition date and time, and automatically generates filenames based on geographic location and timestamp.
The rasterio library handles the geospatial aspects, including CRS and transformation, ensuring that each tile can be correctly referenced geographically.
This script can be easily adapted for other use cases, including different tile sizes or formats like GeoTIFF.

# Current limitations:
resolution of the satelittes images:
On Copernicus, image download must be: Image width and height must be between 1px and 2500px