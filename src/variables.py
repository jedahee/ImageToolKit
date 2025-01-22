from prompt_toolkit.styles import Style

valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

# Definir el estilo para personalizar los márgenes y el espaciado
style = Style([
  ('qmark', 'fg:#32cf4c bold'),       # token in front of the question
  ('question', 'bold'),               # question text
  ('answer', 'fg:#32cf4c bold'),      # submitted answer text behind the question
  ('pointer', 'fg:#673ab7 bold'),     # pointer used in select and checkbox prompts
  ('highlighted', 'fg:white bg:#673ab7 bold'), # pointed-at choice in select and checkbox prompts
  ('selected', 'fg:#32cf4c'),         # style for a selected item of a checkbox
  ('separator', 'fg:#cc5454'),        # separator in lists
  ('instruction', ''),                # user instructions for select, rawselect, checkbox
  ('text', ''),                       # plain text
  ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
])

options_main_menu = {
  'REDUCE': 'Reduce the file size of the image(s)',
  'RESIZE': 'Resize and scale the image(s)',
  'FORMATS': 'Convert image formats (PNG, JPG, JPEG, etc.) or rename the file',
  'FILTERS': 'Apply image filters',
  'TEXT': 'Add text to the image(s)',
  'THUMBNAILS': 'Create image thumbnails',
  'EXIT': 'Exit',
}

available_filters = [
  "SEPIA", "INVERT", "GRAYSCALE", "BLUR", "CONTOUR", "DETAIL",
  "SHARPEN", "EMBOSS", "EDGE_ENHANCE", "SMOOTH", "POSTERIZE",
  "SOLARIZE", "EQUALIZE", "BRIGHTNESS_INC", "BRIGHTNESS_DEC",
  "CONTRAST_INC", "CONTRAST_DEC", "SATURATION_INC", "SATURATION_DEC",
  "ROTATE_90", "ROTATE_180", "FLIP_HORIZONTAL", "FLIP_VERTICAL",
  "CROP_CENTER"
]

msg_allowed = {
  'ERROR': 'error',
  'WARNING': 'warning',
  'INFO': 'info',
  'SUCCESS': 'success'
}

output_path = "new_images"
fonts_dir = 'fonts/'
allowed_limits_kb = ["1500 KB", "1024 KB", "512 KB"]
