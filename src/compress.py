from src.variables import output_path
from src.rescale import rescale_percent
from PIL import Image
import os
import warnings
from pathlib import Path

def compress(input_path, images, can_resize, want_force, max_size):
  input_path = str(input_path)
  input_path += '/' if input_path[-1] != '/' else '';
  max_size = int(max_size[:-2])
  warnings.simplefilter('ignore', Image.DecompressionBombWarning)

  base_dir = Path(__file__).resolve().parent.parent  # Subir dos directorios

  for image in images:
    resize_size_percent = 75
    user_is_info = False
    # Ruta completa de salida para el archivo
    output_path_copy = base_dir / output_path / image

    # Asegúrate de que el directorio de salida exista
    output_path_copy.parent.mkdir(parents=True, exist_ok=True)

    image_open = Image.open(input_path+image)

    extension = os.path.splitext(image)[1][1:]
    extension = "jpeg" if extension == "jpg" else extension

    width, height = image_open.size

    quality = 100
    min_quality_resize = 40
    min_quality = min_quality_resize if not want_force else 5

    if (width >= Image.MAX_IMAGE_PIXELS or height >= Image.MAX_IMAGE_PIXELS) and can_resize:
      image_open = rescale_percent(image_open, 90)
      image_open.save(output_path_copy, format=extension, quality=quality, optimize=True)

    image_size = os.path.getsize(input_path+image) / 1024  # Tamaño en KB

    if image_size < max_size:
      print("Image "+str(image)+" already had a size below the specified KB limit. (Actual size:",round(image_size, 2),"KB)")
      user_is_info = True

    # Si el tamaño es mayor que el máximo permitido, ajustamos la calidad
    while image_size > max_size and quality >= min_quality:
        # Reducir la calidad de la imagen en 5% por cada iteración
        if can_resize and quality <= min_quality_resize:
          if (resize_size_percent == 75):
            image_open = rescale_percent(image_open, resize_size_percent)
            resize_size_percent = 50
          elif (resize_size_percent == 50):
            image_open = rescale_percent(image_open, resize_size_percent)
            resize_size_percent = 25
          elif (resize_size_percent == 25):
            resize_size_percent = 10
            image_open = rescale_percent(image_open, resize_size_percent)

        quality -= 5

        # Guardar la imagen con la nueva calidad
        image_open.save(output_path_copy, format=extension, quality=quality, optimize=True)

        # Comprobar nuevamente el tamaño del archivo
        image_size = os.path.getsize(output_path_copy) / (1024)  # Tamaño en KB

    if not user_is_info:
      print("Image "+ str(image) +" now has a file size of", int(image_size),"KB.")
    else:
      if image_size > max_size:
        print("Image "+str(image)+" could not reach the specified maximum size, it has been reduced to a weight of", int(image_size),"KB.")
