from PIL import Image
from src.variables import msg_allowed
from src.utils import display_msg
import re

def new_format(input_path, selected_output_path, images, new_format, change_name, base_name="none", default_start=1):
  i = 0
  # Extract starting index if provided in the base_name
  start_match = re.search(r"--START\s+(\d+)", base_name)
  start_index = int(start_match.group(1)) if start_match else default_start

  # Clean up the base_name by removing the placeholders
  base_name_cleaned = re.sub(r"--INDEX|--START\s+\d+", "", base_name).strip()

  for image in images:
    if new_format not in image:
      try:
        # Open the image
        with Image.open(str(input_path)+"/"+str(image)) as img:
          # Generate the new file name
          index = start_index + i
          new_file_name = f"{base_name_cleaned}{index}.{new_format.lower()}" if change_name else f"{image.split('.')[0]}.{new_format.lower()}"

          # Save the image in the new format
          img.convert("RGB").save(selected_output_path+"/"+new_file_name, format=new_format.upper())
          display_msg(f"Image {image}: Converted to {new_format} and saved to {selected_output_path}", msg_allowed["SUCCESS"], False)
      except Exception as e:
          display_msg(f"Error processing image {image}: {e}", msg_allowed["ERROR"], False)
    else:
      display_msg(f"Image {image} already has format {new_format}", msg_allowed["INFO"], False)

    i += 1
