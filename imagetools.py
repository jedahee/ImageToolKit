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
  -> Convertir a blanco y negro
  -> Aplicar filtros
    -> Mostrar catálogo de filtros
    -> Pedir filtro
  -> Añadir texto a la imagen
    -> Pedir texto a añadir
    -> Pedir fuente (mostrar catálogo)
    -> Pedir color (mostrar catálogo)
    -> Pedir posición del texto en la imagen
  -> Crear miniaturas
    -> Mostrar catálogo de tamaños de miniaturas (ej.: 16px, 32px, 48px, 64px)
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

# Internal import
from src.utils import welcome, select_option, ask_for_path, ask_for_images

def run_interactive_app():
  option_menu = ""
  images_selected = []
  selected_path=" "

  while option_menu.lower() != "exit":
    welcome()
    option_menu = select_option()

    if option_menu.lower() != "exit":
      selected_path = ask_for_path()

      if (selected_path != ".." and selected_path != ""):
        images_selected = ask_for_images(selected_path)
    else:
      print("Bye! :)")

def main():
    # ! PROXIMO CLI
    '''
    # Verificar si se pasaron argumentos al ejecutar el script
    if len(sys.argv) > 1:
        # Si se pasaron argumentos, ejecutar la CLI
        cli()  # Llamamos a la función cli() definida en src/cli.py
    else:
        # Si no se pasaron argumentos, ejecutar la app interactiva
        run_interactive_app()
    '''
    run_interactive_app()

if __name__ == "__main__":
    main()
