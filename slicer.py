import os
import rasterio
import numpy as np
from rasterio.windows import Window
from datetime import datetime
from PIL import Image
import argparse

def slice_satellite_image(image_path, image_file_name, output_dir, tile_size=(256, 256), overlap=0.1):
    """
    Slices a satellite image into smaller tiles with overlap and saves them using a specific naming convention.
    
    Parameters:
    - image_path: str, path to the input satellite image
    - image_file_name: str, name of the input satellite image
    - output_dir: str, directory where tiles will be saved
    - tile_size: tuple of ints, size of the tiles (width, height) in pixels
    - overlap: float, percentage overlap between tiles (0.0 to 1.0)
    """
    full_image_path = os.path.join(image_path, image_file_name)
    
    # Open the satellite image using rasterio
    with rasterio.open(full_image_path) as dataset:
        # Extract metadata
        bounds = dataset.bounds  # geographic bounds of the image
        transform = dataset.transform  # affine transformation for georeferencing
        crs = dataset.crs  # coordinate reference system
        width, height = dataset.width, dataset.height  # image dimensions
        img_date = dataset.tags().get('TIFFTAG_DATETIME', 'unknown')  # get image date if available
        
        # Parse the date, if available
        if img_date != 'unknown':
            img_datetime = datetime.strptime(img_date, '%Y:%m:%d %H:%M:%S')
        else:
            img_datetime = datetime.now()

        # Calculate the overlap in pixels
        overlap_pixels_x = int(tile_size[0] * overlap)
        overlap_pixels_y = int(tile_size[1] * overlap)

        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Iterate over the image and create tiles
        tile_count = 0
        for x in range(0, width, tile_size[0] - overlap_pixels_x):
            for y in range(0, height, tile_size[1] - overlap_pixels_y):
                # Ensure we don't exceed the image dimensions
                if x + tile_size[0] > width:
                    x = width - tile_size[0]
                if y + tile_size[1] > height:
                    y = height - tile_size[1]
                
                # Calculate the window for this tile
                window = Window(x, y, tile_size[0], tile_size[1])
                tile = dataset.read(window=window)

                # Convert the tile to an image using PIL for saving as PNG
                tile_img = Image.fromarray(tile.transpose(1, 2, 0))
                
                # Calculate the geographic coordinates of the upper-left corner of the tile
                ul_x, ul_y = transform * (x, y)
                
                # Format geographic coordinates into UTM-like system (this example assumes UTM-based data)
                utm_zone = crs.to_string().split(':')[-1]  # Extract the UTM zone (example for UTM)
                tile_latitude = ul_y
                tile_longitude = ul_x

                # Construct the filename for the tile
                tile_filename = (
                    f"tile_UTM{utm_zone}_{int(tile_longitude)}E_{int(tile_latitude)}N_"
                    f"{img_datetime.strftime('%Y%m%dT%H%M%S')}_{tile_size[0]}x{tile_size[1]}.png"
                )
                
                # Save the tile
                tile_output_path = os.path.join(output_dir, tile_filename)
                tile_img.save(tile_output_path)
                tile_count += 1
                
        print(f"Created {tile_count} tiles in '{output_dir}'.")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Slice a satellite image into tiles with overlap.")
    parser.add_argument('--image_path', type=str, default='.', help='Directory where the satellite image is located')
    parser.add_argument('--image_file_name', type=str, default='satellite_image.tif', help='The satellite image file name')
    parser.add_argument('--output_path', type=str, default='./output_tiles', help='Directory to save the sliced tiles')
    parser.add_argument('--tile_size', type=int, nargs=2, default=[256, 256], help='Tile size as (width, height)')
    parser.add_argument('--overlap', type=float, default=0.1, help='Percentage overlap between tiles (0.0 to 1.0)')
    
    args = parser.parse_args()

    # Call the function to slice the image
    slice_satellite_image(
        image_path=args.image_path, 
        image_file_name=args.image_file_name, 
        output_dir=args.output_path, 
        tile_size=tuple(args.tile_size),
        overlap=args.overlap
    )

if __name__ == '__main__':
    main()
