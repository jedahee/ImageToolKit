from src.utils import display_msg
from src.variables import fonts_dir, msg_allowed, output_path
import questionary
import os
from PIL import Image, ImageDraw, ImageFont

# Function to get available fonts in the fonts directory
def get_available_fonts():
    fonts = []
    for file in os.listdir(fonts_dir):
        if file.endswith(".ttf") or file.endswith(".otf"):  # Only TrueType or OpenType fonts
            fonts.append(file)
    return fonts

def add_text_to_image(input_path, images, text_to_add, position_choice, font_choice, font_size_ratio, color_choice):
    input_path = str(input_path)
    input_path += '/' if input_path[-1] != '/' else ''

    # Process the selected images
    for image in images:
        try:
            with Image.open(input_path + image) as img:
                # Get image dimensions
                img_width, img_height = img.size

                # Calculate font size as a percentage of the image width
                font_size = int((font_size_ratio / 100) * img_width)

                # Load the font
                font_path = os.path.join(fonts_dir, font_choice)
                font = ImageFont.truetype(font_path, font_size)

                # Calculate relative position
                position_mapping = {
                    "Top Left": (0.1 * img_width, 0.1 * img_height),
                    "Top Right": (0.9 * img_width, 0.1 * img_height),
                    "Center": (0.5 * img_width, 0.5 * img_height),
                    "Bottom Left": (0.1 * img_width, 0.9 * img_height),
                    "Bottom Right": (0.9 * img_width, 0.9 * img_height)
                }
                position = position_mapping[position_choice]

                # Create a drawing object
                draw = ImageDraw.Draw(img)

                # Add the text
                draw.text(position, text_to_add, font=font, fill=color_choice)

                # Save the image with the added text
                img.save(output_path + "/" + image)

                display_msg(f"Text added to image {image} and saved to {output_path}", msg_allowed["SUCCESS"], False)
        except Exception as e:
            display_msg(f"Error adding text to image {image}: {e}", msg_allowed["ERROR"], False)
