
from deface.filter.filter import filter_blur
from deface.filter.filter import filter_pixelate
from deface.filter.filter import filter_line_mosaic
from deface.filter.filter import filter_facet_effect
from deface.filter.filter import filter_verwischung_1

def filter(roi, filter_name):
  match filter_name:
    case 'blur':
      return filter_blur(roi)
    case 'pixelate':
      return filter_pixelate(roi)
    case 'line_mosaic':
      return filter_line_mosaic(roi)
    case 'facet_effect':
      return filter_facet_effect(roi)
    case 'verwischung_1':
      return filter_verwischung_1(roi)
    case _:
      # Handle unknown filter names or default case if necessary
      print(f"Unknown filter: {filter_name}")
      return roi # Return original ROI or handle error
