from src.utils import display_msg
from src.variables import msg_allowed, output_path
from PIL import Image
import os

# Function to resize an image to a fixed width and height
def resize_fixed(image, new_width, new_height, quality_type):
  """Resize the image to fixed width and height."""
  return image.resize((new_width, new_height), quality_type)

# Function to rescale an image proportionally by a percentage
def rescale_percent(image, resize_size_percent):
  """Rescale the image proportionally by a percentage."""
  width, height = image.size
  new_width = int((resize_size_percent * width) / 100)
  new_height = int((resize_size_percent * height) / 100)
  return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Function to process images for resizing based on mode (fixed or percentage)
def process_images_resize(input_path, images, resize_mode, resize_value, quality_type):
  input_path = str(input_path)
  input_path += '/' if input_path[-1] != '/' else ''

  for image in images:
    try:
      with Image.open(input_path + image) as img:
        width, height = img.size
        extension = os.path.splitext(image)[1][1:]
        extension = "jpeg" if extension.lower() == "jpg" else extension.lower()

        # Handle resize modes
        if resize_mode == "fixed":
          new_width, new_height = resize_value
          if new_width > width or new_height > height:
            display_msg(
              f"Warning: Resizing {image} to larger dimensions may result in quality loss",
              msg_allowed["INFO"], False
            )
          resized_img = resize_fixed(img, new_width, new_height, quality_type)
        elif resize_mode == "percent":
          resized_img = rescale_percent(img, resize_value)
        else:
          raise ValueError("Invalid resize mode. Use 'fixed' or 'percent'")

        # Save the resized image
        resized_img.save(output_path + "/" + image, optimize=True, format=extension)
        display_msg(
          f"Image {image} resized and saved to {output_path}.",
          msg_allowed["SUCCESS"], False
        )
    except Exception as e:
      display_msg(f"Error processing image {image}: {e}", msg_allowed["ERROR"], False)

# Function to create thumbnails of images
def thumbnails(input_path, images, want_favicon, thumbnail_size):
  input_path = str(input_path)
  input_path += '/' if input_path[-1] != '/' else ''

  for image in images:
    try:
      with Image.open(input_path + image) as img:
        width, height = img.size

        # Set the extension for favicon (ICO) or other image formats
        extension = "ico" if want_favicon.lower() == "yes" else os.path.splitext(image)[1][1:].lower().replace("jpg", "jpeg")
        output_filename = f"{os.path.splitext(image)[0]}.{extension}"

        # Resize the image if necessary
        if width > thumbnail_size and height > thumbnail_size:
          img_resized = img.resize((thumbnail_size, thumbnail_size))

          # Save the resized image with the correct format
          img_resized.save(output_path + "/" + output_filename, optimize=True, format=extension)
          display_msg(
              f"Image {image} successfully resized to {thumbnail_size}px and saved as {output_filename} in {output_path}",
              msg_allowed["SUCCESS"],
              False
          )
        else:
          display_msg(
              f"Image {image} is already {thumbnail_size}px or smaller. No resizing needed",
              msg_allowed["INFO"],
              False
          )

    except Exception as e:
      display_msg(f"Error processing image {image}: {e}", msg_allowed["ERROR"], False)
