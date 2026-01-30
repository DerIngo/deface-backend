import os
import cv2
from deface.filter.filter_select import filter
from deface.paste.paste_select import paste_ellipse

from deface.common.config import FOLDER_CONFIG
from deface.model import model


def anonymizeImage(img, filter_name, paste_ellipse_name):
    results = model.predict(img, conf=0.25)
    
    for result in results:
        for box in result.boxes:
            # Koordinaten der Box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1
            
            # 2. Den Bereich (ROI) extrahieren und anonymisieren
            roi = img[y1:y2, x1:x2]
            if roi.size == 0: continue
            
            # Filter auf dem gesamten Rechteck (temporär)
            filtered_roi = filter(roi, filter_name)
            if filtered_roi.size == 0: continue
            
            # gefiltertes Rechteck einfügen
            paste_ellipse(img, roi, filtered_roi, 
                  x1, y1, x2, y2,
                  w, h,
                  paste_ellipse_name)
                
    return img


def anonymize(input_file_name, filter_name, paste_ellipse_name):
    input_base_dir = FOLDER_CONFIG['upload']
    output_base_dir = FOLDER_CONFIG['result']

    output_dir = f"{output_base_dir}/{filter_name}/{paste_ellipse_name}"
    os.makedirs(output_dir, exist_ok=True)

    image_path = f"{input_base_dir}/{input_file_name}"
    result_path = f"{output_dir}/{input_file_name}"

    # WICHTIG: Zielordner rekursiv anlegen
    result_dir = os.path.dirname(result_path)
    os.makedirs(result_dir, exist_ok=True)

    image = cv2.imread(image_path)

    result_image = anonymizeImage(image, filter_name, paste_ellipse_name)
    cv2.imwrite(result_path, result_image)

    result_file = os.path.relpath(result_path, output_base_dir)
    return result_file
