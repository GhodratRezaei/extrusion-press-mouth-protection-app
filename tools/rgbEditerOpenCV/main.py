from PIL import Image
import numpy as np

# Open the image file
input_image_path = 'input_image.jpg'
output_image_path = 'logo.PNG'
image = Image.open(input_image_path)

# Ensure the image is in RGB mode
image = image.convert('RGB')

# Convert the image to a numpy array
data = np.array(image)

# Define the target color and replacement color
target_rgb = np.array([207, 194, 188])
replacement_rgb = np.array([220, 220, 240])

# Define a tolerance for color matching
tolerance = 10

# Find the pixels that are within the tolerance range of the target RGB color
match_pixels = np.all(np.abs(data - target_rgb) <= tolerance, axis=-1)

# Replace the target color with the replacement color
data[..., :3][match_pixels] = replacement_rgb

# Convert the numpy array back to an image
output_image = Image.fromarray(data, 'RGB')

# Save the output image in RGB format
output_image.save(output_image_path)

print(f"Image processed and saved as {output_image_path}")
