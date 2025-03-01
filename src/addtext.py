from src.utils import display_msg
from src.variables import fonts_dir, msg_allowed
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

from PIL import Image, ImageDraw, ImageFont
import os
from src.utils import display_msg
from src.variables import fonts_dir, msg_allowed

def add_text_to_image(input_path, selected_output_path, images, text_to_add, position_choice, font_choice, font_size_ratio, color_choice):
    input_path = str(input_path)
    if not input_path.endswith('/'):
        input_path += '/'

    for image in images:
        try:
            with Image.open(input_path + image) as img:
                img_width, img_height = img.size

                font_size = int((font_size_ratio / 100) * img_width)
                font_path = os.path.join(fonts_dir, font_choice)
                font = ImageFont.truetype(font_path, font_size)

                draw = ImageDraw.Draw(img)

                # Medir el tamaño real del texto
                text_bbox = draw.textbbox((0, 0), text_to_add, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                # Ajustar posición según el texto
                if position_choice == "Top Left":
                    position = (10, 10)  # Margen pequeño
                elif position_choice == "Top Right":
                    position = (img_width - text_width - 10, 10)
                elif position_choice == "Center":
                    position = ((img_width - text_width) // 2, (img_height - text_height) // 2)
                elif position_choice == "Bottom Left":
                    position = (10, img_height - text_height - 10)
                elif position_choice == "Bottom Right":
                    position = (img_width - text_width - 10, img_height - text_height - 10)
                else:
                    position = (10, 10)  # fallback

                # Dibujar el texto en la posición ajustada
                draw.text(position, text_to_add, font=font, fill=color_choice)

                # Guardar la imagen modificada
                os.makedirs(selected_output_path, exist_ok=True)
                img.save(os.path.join(selected_output_path, image))

                display_msg(f"Text added to image {image} and saved to {selected_output_path}", msg_allowed["SUCCESS"], False)

        except Exception as e:
            display_msg(f"Error adding text to image {image}: {e}", msg_allowed["ERROR"], False)
