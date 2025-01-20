from src.utils import display_msg
from src.variables import fonts_dir, msg_allowed, output_path
import questionary
import os
from PIL import Image, ImageDraw, ImageFont

# Función para obtener las fuentes disponibles en la carpeta fonts
def get_available_fonts():
  fonts = []
  for file in os.listdir(fonts_dir):
    if file.endswith(".ttf") or file.endswith(".otf"):  # Sólo fuentes TrueType o OpenType
      fonts.append(file)
  return fonts

def add_text_to_image(input_path, images, text_to_add, position_choice, font_choice, font_size_ratio, color_choice):
  input_path = str(input_path)
  input_path += '/' if input_path[-1] != '/' else ''

  # Procesar las imágenes seleccionadas
  for image in images:
    try:
      with Image.open(input_path + image) as img:
        # Obtener dimensiones de la imagen
        img_width, img_height = img.size

        # Calcular tamaño de la fuente como un porcentaje del ancho
        font_size = int((font_size_ratio/100) * img_width)

        # Cargar la fuente
        font_path = os.path.join(fonts_dir, font_choice)
        font = ImageFont.truetype(font_path, font_size)

        # Calcular la posición relativa
        position_mapping = {
          "Top Left": (0.1 * img_width, 0.1 * img_height),
          "Top Right": (0.9 * img_width, 0.1 * img_height),
          "Center": (0.5 * img_width, 0.5 * img_height),
          "Bottom Left": (0.1 * img_width, 0.9 * img_height),
          "Bottom Right": (0.9 * img_width, 0.9 * img_height)
        }
        position = position_mapping[position_choice]
        # Crear un objeto de dibujo
        draw = ImageDraw.Draw(img)

        # Añadir el texto
        draw.text(position, text_to_add, font=font, fill=color_choice)

        # Guardar la imagen con el texto añadido
        img.save(output_path + "/" + image)

        display_msg(f"Text added to image {image} and saved to {output_path}", msg_allowed["SUCCESS"], False)
    except Exception as e:
      display_msg(f"Error adding text to image {image}: {e}", msg_allowed["ERROR"], False)
