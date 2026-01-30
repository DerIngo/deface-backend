import glob
import os
import cv2
#from google.colab.patches import cv2_imshow
from deface.anonymize import anonymize

from deface.common.config import FOLDER_CONFIG

def process_all_images(input_dir, filter_name, paste_ellipse_name):
    input_base_dir = FOLDER_CONFIG['upload']
    image_paths = glob.glob(f"{input_base_dir}/{input_dir}/*.jpg")
    print(f"Starte Verarbeitung von {len(image_paths)} Bildern...")

    for path in image_paths:
        print(f"path: {path}")
        # "upload/" entfernen
        relative_path = os.path.relpath(path, input_base_dir)
        print(f"relative_path: {relative_path}")
        # Filter face
        result_path = anonymize(relative_path, filter_name, paste_ellipse_name)
        print(f"result_path: {result_path}")
        # load filtered Image         
        result_image = cv2.imread(result_path)
        print(f"Fertig: {result_path}")
        #cv2_imshow(result_image)

# Startbefehl
process_all_images('test_samples', 'verwischung_1', 'hard')