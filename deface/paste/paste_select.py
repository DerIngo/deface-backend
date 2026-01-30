from deface.paste.paste import paste_ellipse_feathered
from deface.paste.paste import paste_ellipse_hard


def paste_ellipse(img, roi, filtered_roi, 
                  x1, y1, x2, y2,
                  w, h,
                  paste_ellipse_name):
  match paste_ellipse_name:
    case 'feathered':
      return paste_ellipse_feathered(img, roi, filtered_roi, x1, y1, x2, y2)
    case 'hard':
      return paste_ellipse_hard(img, roi, filtered_roi, x1, y1, x2, y2, w, h)
    case _:
      # Handle unknown filter names or default case if necessary
      print(f"Unknown filter: {paste_ellipse_name}")
      return roi # Return original ROI or handle error
