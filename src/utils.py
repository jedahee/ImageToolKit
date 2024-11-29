import questionary
import os
from pathlib import Path
from sys import exit

from src.variables import valid_extensions, style, options_main_menu, errors_allowed

def welcome():
  print("""
 █████
░░███
 ░███  █████████████    ██████    ███████  ██████
 ░███ ░░███░░███░░███  ░░░░░███  ███░░███ ███░░███
 ░███  ░███ ░███ ░███   ███████ ░███ ░███░███████
 ░███  ░███ ░███ ░███  ███░░███ ░███ ░███░███░░░
 █████ █████░███ █████░░████████░░███████░░██████
░░░░░ ░░░░░ ░░░ ░░░░░  ░░░░░░░░  ░░░░░███ ░░░░░░
                                 ███ ░███
                                ░░██████
                                 ░░░░░░
 ███████████                   ████
░█░░░███░░░█                  ░░███
░   ░███  ░   ██████   ██████  ░███   █████
    ░███     ███░░███ ███░░███ ░███  ███░░
    ░███    ░███ ░███░███ ░███ ░███ ░░█████
    ░███    ░███ ░███░███ ░███ ░███  ░░░░███
    █████   ░░██████ ░░██████  █████ ██████
   ░░░░░     ░░░░░░   ░░░░░░  ░░░░░ ░░░░░░
""")

def select_option():
  option = questionary.select(
    "What do you want ImageTools to do for you?",
    choices=list(options_main_menu.values()),
    style=style
  ).ask()

  return select_option() if option == None else option

def ask_for_path():
  print("Note: Type '..' to back menu list")
  try:
    q_path = questionary.text("Please enter the directory path:", style=style).ask()

    if q_path == "..":
      return q_path

    input_path = Path(q_path)
  except TypeError:
    print("There was an error with the path")
    return ask_for_path()

  if input_path.exists():
    return input_path
  else:
    print("The path does not exist. Please enter a valid path.")
    return ask_for_path()

def ask_for_images(path):

  images_dir = []
  selected_images_dir = []

  try:
    object_path = Path(path)
  except:
    print("There seems to be an issue with this path. Please try again later or verify that it exists.")

  # Recorrer todos los archivos en el directorio
  for file_path in path.iterdir():
      # Verificar si el archivo tiene una extensión válida de imagen
      if file_path.suffix.lower() in valid_extensions:
        images_dir.append(file_path.name)

  if len(images_dir) == 0:
    print("Sorry! No images found in this path :C")
    exit()

  selected_images_dir = questionary.checkbox(
    'Select image files',
    choices=images_dir,
    style=style
  ).ask()

  return ask_for_images(path) if selected_images_dir == None else selected_images_dir


def qselect(message, options):
  return questionary.select(
    message,
    choices=options,
    style=style
  ).ask()

def display_msg(msg, type_msg):
  color = ""
  if type_msg == 'error':
      color = "\033[37m\033[41m"  # Texto blanco (37m), fondo rojo (41m)
  elif type_msg == 'warning':
      color = "\033[37m\033[43m"  # Texto blanco (37m), fondo amarillo (43m)
  elif type_msg == 'info':
      color = "\033[37m\033[44m"  # Texto blanco (37m), fondo azul (44m)
  elif type_msg == 'success':
      color = "\033[37m\033[42m"  # Texto blanco (37m), fondo verde (42m)

  # Imprimir el mensaje con los colores de texto y fondo
  print(f"{color}{msg}\033[0m")  # \033[0m es para resetear los estilos
