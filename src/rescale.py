from PIL import Image

def rescale_percent(image, resize_size_percent):
  width, height = image.size
  new_width = int((resize_size_percent * width) / 100)
  new_height = int((resize_size_percent * height) / 100)
  return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
