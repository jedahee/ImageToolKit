'''
--------------------
IMAGE TOOLS APP v0.1
--------------------
Author github name: jedahee
Author name: Jesús Daza

Image Tools es una aplicación de consola la cual ofrece múltiples herramientas
para poder editar una o mñas imágenes de forma rápida y sencilla.

¿Que puede hacer Image Tools por ti?

1) Reducir el peso de la(s) imagen(es)
2) Redimensionar y cambiar la escala
3) Conversor de extensión (png, jpg, jpeg...)
4) Convertir a blanco y negro
5) Aplicar filtros
6) Añadir texto a la imagen
7) Crear miniaturas

---

Flujo de Image Tools:

-> Entrada al script
  -> Mensaje de bienvenida
  -> (Usuario elige opción correcta del catálogo) - (Muestra listado)
  -> (Usuario especifica la ruta que contiene sus imágenes)
  -> (Usuario selecciona que imágenes quiere editar)

  Si el usuario eligió:
  -> Reducir el peso de la(s) imagen(es)
    -> ¿Por debajo de que tamaño quieres que Image Tools lo reduzca? (ej.: 512KB | siempre en KB)
    -> ¿Si hay imágenes con demasiado tamaño, puede Image Tools reescarla y hacerla más pequeña?
    -> ¿Si la imagen es demasiado pesada, quieres forzar la reducción de tamaño al límite especificado en KB sacrificando algo de calidad?
  -> Redimensionar (valor fijo) o reescalar (valor proporcional)
    -> Redimensionar
      -> Mostrar aviso de que si se redimensiona a una escala mayor a la de la imagen original puede perder calidad
      -> Pediar ancho + alto
      -> Pedir tipo de calidad (Avisando del tiempo de espera)
    -> Cambiar escala
      -> Pedir proporción de la nueva imagen (50%, 75% o 150%...)
  -> Conversor de extensión (png, jpg, jpeg...) - También puedes cambiar el nombre
    -> Mostrar comodines disponibles para los nombres (por ej.: index con -INDEX, -INEX_START para indicar el inicio del contenio del index)
    -> Pedir nuevo (o nuevos) nombres
    -> Pedir nueva extensión
  -> Aplicar filtros
    -> Mostrar catálogo de filtros
    -> Pedir filtro
  -> Añadir texto a la imagen
    -> Pedir texto a añadir
    -> Pedir fuente (mostrar catálogo)
    -> Pedir color (mostrar catálogo)
    -> Pedir posición del texto en la imagen
  -> Crear miniaturas (favicon)
    -> Mostrar catálogo de tamaños de miniaturas (ej.: 16px, 32px, 48px, 64px)
    -> Preguntar si quieres tranformar los archivos a .ICO
    -> Pedir tamaño de la miniatura

 -> Muestra información del estado de la opción ejecutada
-> Salida al script

---

Estructura del proyecto:

imagetools/
├── env/                # Entorno virtual (no se debe versionar, por ejemplo, en .gitignore)
├── src/                # Módulo principal de la herramienta
│   ├── __init__.py     # Inicializador del paquete
│   ├── cli.py          # ! Código para la interfaz de línea de comandos (argumentos y ejecución) - PRÓXIMO
│   ├── rescale.py      # Funciones relacionadas con el reescalado de imágenes
│   ├── compress.py     # Funciones para ajustar el tamaño/comprimir imágenes
│   ├── addtext.py      # Funciones para añadir texto a las imágenes
│   ├── extension.py    # Funciones para editar el nombre y extensión de imágenes
│   ├── color.py        # Funciones para manipular colores (ajustes de color, blanco y negro, etc.)
│   └── utils.py        # Funciones auxiliares y herramientas generales (por ejemplo, validación de rutas, manejo de errores)
├── new_images/         # Carpeta para almacenar imágenes procesadas (salida)
├── requirements.txt    # Dependencias del proyecto (Pillow, click, etc.)
├── README.md           # Documentación del proyecto
├── setup.py            # Configuración del paquete si planeas distribuirlo
├── imagetools.py       # Punto de entrada principal si no se utiliza el CLI
└── .gitignore          # Archivos a ignorar en el control de versiones (entorno, etc.)


'''
import questionary
import warnings
from PIL import Image
from time import sleep
import os, sys

# Internal import
from src.utils import welcome, select_option, ask_for_path, ask_for_images, qselect, display_msg
from src.compress import compress
from src.extension import new_format
from src.variables import style, options_main_menu, allowed_limits_kb, msg_allowed, available_filters
from src.color import apply_filter_to_images
from src.rescale import thumbnails, process_images_resize
from src.addtext import get_available_fonts, add_text_to_image
from src.cli import cli

def run_interactive_app():
  images_selected = []
  option_menu = ""
  format_selected = ""
  selected_path= ""
  base_name = ""

  warnings.simplefilter('ignore', Image.DecompressionBombWarning)

  while option_menu != options_main_menu["EXIT"]:
    welcome()
    option_menu = select_option()

    if option_menu != options_main_menu["EXIT"]:
      selected_path = ask_for_path()

      if (selected_path != ".." and selected_path != ""):
        images_selected = ask_for_images(selected_path)

        if option_menu == options_main_menu["REDUCE"]:
          max_size = qselect("Choose the maximum image size:", allowed_limits_kb)
          can_resize = qselect("If the image exceeds an appropriate size, do you authorize Image Tools to resize it to a smaller dimension?", ["Yes", "No"])
          want_force = qselect("If the image is too large, would you like to force the size reduction to the specified KB limit, sacrificing some quality?", ["Yes", "No"])

          can_resize = True if can_resize.lower() == "yes" else False
          want_force = True if want_force.lower() == "yes" else False

          print()

          compress(selected_path, images_selected, can_resize, want_force, max_size)

        elif option_menu == options_main_menu["RESIZE"]:
          resize_mode = qselect(
            "Choose resize mode:",
            ["Fixed size", "Proportional scale"]
          ).lower()

          if resize_mode == "fixed size":
            display_msg(
                "Note: Resizing to larger dimensions may result in quality loss",
                msg_allowed["INFO"], False
            )

            try:
              new_width = int(questionary.text("Enter the new width (px):").ask())
              new_height = int(questionary.text("Enter the new height (px):").ask())

              quality_type = qselect(
                "Choose image quality (faster processing or better quality):",
                ["Normal (fast)", "High (slower processing)"]
              ).lower()

              quality_mapping = {
                  "normal (fast)": Image.Resampling.BICUBIC,
                  "high (slower processing)": Image.Resampling.LANCZOS,
              }

              quality = quality_mapping[quality_type]

              process_images_resize(
                  selected_path, images_selected, "fixed",
                  (new_width, new_height), quality
              )
            except Exception as e:
              print()
              display_msg(f"Invalid input! Please enter a valid numeric value for the width and height", msg_allowed["ERROR"], False)
              print()

          elif resize_mode == "proportional scale":
            try:
              scale_percent = int(
                  questionary.text(
                      "Enter the scaling percentage (e.g., 50, 75, 150):"
                  ).ask()
              )

              process_images_resize(
                selected_path, images_selected, "percent",
                scale_percent, None
              )
            except Exception as e:
              print()
              display_msg(f"Invalid input! Please enter a valid numeric value for the width and height", msg_allowed["ERROR"], False)
              print()

        elif option_menu == options_main_menu["FORMATS"]:
          format_selected = qselect("Select the format to convert to:", ["JPEG", "PNG", "BMP"])
          change_name = qselect("Do you want to rename the files?", ["Yes", "No"])
          change_name = True if change_name.lower() == "yes" else False

          if change_name:
            print("\nYou can use the following placeholders:")
            print(" --INDEX: Adds an index to the end of the new file name, starting from 1. (default)")
            print(" --START <number>: Adds an index to the end of the new file name, starting from the specified <number>.")

            while base_name == "":
              base_name = questionary.text("Enter the new base name for your files:", style=style).ask()

          new_format(selected_path, images_selected, format_selected, change_name, base_name)
          base_name = ""
        elif option_menu == options_main_menu["FILTERS"]:

          # Pedir al usuario que seleccione un filtro
          filter_choice = qselect(
            "Choose a filter to apply:",
            available_filters
          )

          # Aplicar el filtro a las imágenes seleccionadas
          apply_filter_to_images(selected_path, images_selected, filter_choice)
        elif option_menu == options_main_menu["TEXT"]:
          # Solicitar al usuario el texto a añadir
          text_to_add = questionary.text("Enter the text to add to the image:").ask()

          # Listar fuentes disponibles en la carpeta "fonts"
          available_fonts = get_available_fonts()

          if not available_fonts:
            display_msg("No fonts found in the fonts directory!", msg_allowed["ERROR"], False)
            font_choice = "Anton.ttf"
          else:
            # Pedir al usuario seleccionar una fuente
            font_choice = qselect("Choose the font for the text:", available_fonts)

          try:
            # Pedir el tamaño de la fuente
            font_size_ratio = float(questionary.text(
              "Enter the font size ratio (e.g., 5%, 15%, 30% of image width):"
            ).ask())
          except Exception as e:
            font_size_ratio = 25
            display_msg(f"Invalid input! Please enter a valid numeric value for the width and height", msg_allowed["ERROR"], False)

          # Pedir el color del texto
          color_choice = qselect(
            "Choose the color of the text:",
            ["black", "white", "red", "blue", "green"]
          )

          # Definir las posiciones posibles
          position_choices = {
            "Top Left": "Top Left",
            "Top Right": "Top Right",
            "Center": "Center",
            "Bottom Left": "Bottom Left",
            "Bottom Right": "Bottom Right"
          }

          # Preguntar por la posición del texto
          position_choice = qselect(
            "Choose the position of the text:",
            list(position_choices.keys())
          )

          # Obtener las coordenadas de la posición elegida
          position = position_choices[position_choice]

          add_text_to_image(selected_path, images_selected, text_to_add, position, font_choice, font_size_ratio, color_choice)

        elif option_menu == options_main_menu["THUMBNAILS"]:
          thumbnail_size = qselect("Choose the desired size for your favicon or thumbnail:", ["16px", "24px", "32px", "48px", "64px", "92px", "128px"])
          want_favicon = qselect(
            "Would you like to convert the images to .ico format for use as favicons?",
            ["Yes", "No"]
          ).lower()
          thumbnails(selected_path, images_selected, want_favicon, int(thumbnail_size[:-2]))

        sleep(1.5)

    else:
      display_msg("All new images are saved in ./new_images", msg_allowed["INFO"])
      display_msg("Bye! :)", msg_allowed["INFO"], False)


def main():
    # ! PROXIMO CLI

    # Verificar si se pasaron argumentos al ejecutar el script
    if len(sys.argv) > 1:
        # Si se pasaron argumentos, ejecutar la CLI
        cli()  # Llamamos a la función cli() definida en src/cli.py
    else:
        # Si no se pasaron argumentos, ejecutar la app interactiva
        run_interactive_app()

    # run_interactive_app()

if __name__ == "__main__":
    main()
