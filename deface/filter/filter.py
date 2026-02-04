import cv2
import numpy as np


def filter_blur(roi):
  h, w = roi.shape[:2]
  # Adaptive Kernel-Größe basierend auf ROI-Größe
  # Bei kleinen ROIs: kleinerer Kernel
  kernel_size = max(3, min(81, int((h + w) / 4)))
  if kernel_size % 2 == 0:
    kernel_size += 1
  return cv2.medianBlur(roi, kernel_size)

def filter_pixelate(roi, pixel_size=None):
    """Verpixelt einen gegebenen Bildausschnitt (ROI) und gibt ihn zurück."""
    # Erhalte Höhe und Breite des ROI
    h, w = roi.shape[:2]
    
    # Adaptive Pixel-Größe basierend auf ROI-Größe
    if pixel_size is None:
        # Bei kleinen ROIs: Pixel_size = 2-3, bei großen: 10-15
        avg_size = (h + w) / 2
        if avg_size < 50:
            pixel_size = 2
        elif avg_size < 100:
            pixel_size = 3
        elif avg_size < 200:
            pixel_size = 5
        else:
            pixel_size = 10

    # Sicherstellen, dass die verkleinerte Größe mindestens 1x1 Pixel ist
    small_width = max(1, w // pixel_size)
    small_height = max(1, h // pixel_size)

    # 1. Herunterskalieren
    small = cv2.resize(roi, (small_width, small_height),
                      interpolation=cv2.INTER_LINEAR)

    # 2. Wieder auf Originalgröße hochskalieren
    pixelated_roi = cv2.resize(small, (w, h),
                               interpolation=cv2.INTER_NEAREST)

    return pixelated_roi  # Nur den verpixelten ROI zurückgeben



def filter_line_mosaic(roi, cell_size=None, edge_intensity=0.7):
    """
    Erzeugt einen linienbasierten Mosaikeffekt.
    - cell_size: Größe der Mosaikzellen (je kleiner, feinere Linien)
    - edge_intensity: Stärke der Kantenhervorhebung (0.0-1.0)
    """
    h, w = roi.shape[:2]
    
    # Adaptive cell_size basierend auf ROI-Größe
    if cell_size is None:
        avg_size = (h + w) / 2
        if avg_size < 50:
            cell_size = 5
        elif avg_size < 100:
            cell_size = 8
        elif avg_size < 200:
            cell_size = 12
        else:
            cell_size = 15

    # 1. Zuerst normal verpixeln (Grundlage)
    # Sicherstellen, dass die Zellgröße nicht zu groß ist
    cell_width = max(3, w // cell_size)
    cell_height = max(3, h // cell_size)

    # Stark herunterskalieren für Blockeffekt
    small = cv2.resize(roi, (cell_width, cell_height),
                      interpolation=cv2.INTER_LINEAR)
    # Wieder hochskalieren
    pixelated = cv2.resize(small, (w, h),
                          interpolation=cv2.INTER_NEAREST)

    # 2. Kanten im ORIGINAL-ROI detektieren (für feine Linien)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Starke Kantendetektion mit Canny
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)

    # Kanten etwas verdicken für bessere Sichtbarkeit
    kernel = np.ones((2, 2), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

    # 3. Kanten auf das verpixelte Bild übertragen
    # Kantenmaske erstellen (Weiß = Kante, Schwarz = Hintergrund)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Mischung: Verpixeltes Bild mit Kanten kombinieren
    # Option A: Kanten als schwarze Linien auf verpixelten Blöcken
    result = pixelated.copy()
    result[edges > 0] = [0, 0, 0]  # Schwarze Linien

    # Option B: Kanten als weiße Linien (wie in vielen Apps)
    # result = pixelated.copy()
    # result[edges > 0] = [255, 255, 255]  # Weiße Linien

    # Option C: Sanfte Überblendung
    # result = cv2.addWeighted(pixelated, 1-edge_intensity,
    #                          edges_colored, edge_intensity, 0)

    return result


def filter_facet_effect(roi, k=None):
    """
    Erzeugt einen facettierten Effekt durch Farbquantisierung
    und Konturhervorhebung.
    - k: Anzahl der Farben (weniger = stärkere Facetten)
    """
    # Adaptive k basierend auf ROI-Größe
    if k is None:
        h, w = roi.shape[:2]
        area = h * w
        if area < 1000:
            k = 4  # Weniger Farben für stärkere Facetten bei kleinen ROIs
        elif area < 5000:
            k = 6
        elif area < 20000:
            k = 8
        else:
            k = 12  # Mehr Farben für feinere Details bei großen ROIs
    
    # 1. Farben reduzieren (Quantisierung)
    data = roi.reshape((-1, 3)).astype(np.float32)

    # K-Means für Farbquantisierung
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 10,
                                    cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    quantized = centers[labels.flatten()].reshape(roi.shape)

    # 2. Konturen der Farbblöcke finden
    gray = cv2.cvtColor(quantized, cv2.COLOR_BGR2GRAY)

    # Leichte Weichzeichnung für glattere Konturen
    blurred = cv2.medianBlur(gray, 5)

    # Adaptive Schwelle für Konturen
    edges = cv2.adaptiveThreshold(blurred, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY_INV, 11, 2)

    # 3. Konturen auf das quantisierte Bild zeichnen
    result = quantized.copy()
    result[edges > 0] = [0, 0, 0]  # Schwarze Konturen

    return result

def filter_verwischung_1(roi,
                         k=None,
                         band_factor=None,
                         post_sigma_x=None,
                         post_sigma_y=None):
    """
    Verwischung_1: starker horizontaler Wisch (Motion/Box blur entlang X)
    + optionales Banding (runterskalieren in Y + nearest hoch)
    + leichtes Nachglätten.
    """

    if roi is None or roi.size == 0:
        return roi

    h, w = roi.shape[:2]
    
    # Adaptive Parameter basierend auf ROI-Größe
    if k is None:
        if w < 50:
            k = 7
        elif w < 100:
            k = 15
        elif w < 200:
            k = 35
        else:
            k = 65
    
    if band_factor is None:
        if h < 50:
            band_factor = 3
        elif h < 100:
            band_factor = 5
        else:
            band_factor = 10
    
    if post_sigma_x is None:
        post_sigma_x = 1.2
    
    if post_sigma_y is None:
        post_sigma_y = 0.6

    # --- A) Horizontaler Motion/Box-Blur
    # Kernel: 1 x k
    k = int(max(3, k))
    if k % 2 == 0:
        k += 1  # ungerade ist oft stabiler/optisch angenehmer

    kernel = np.ones((1, k), dtype=np.float32) / k
    blurred = cv2.filter2D(roi, ddepth=-1, kernel=kernel, borderType=cv2.BORDER_REPLICATE)

    # --- B) Banding/Scanline-Optik (optional)
    # band_factor > 1: je kleiner, desto stärkere Streifen
    if band_factor and band_factor > 1:
        small_h = max(2, h // int(band_factor))
        tmp = cv2.resize(blurred, (w, small_h), interpolation=cv2.INTER_AREA)
        blurred = cv2.resize(tmp, (w, h), interpolation=cv2.INTER_NEAREST)

    # --- C) leichtes Nachglätten (nimmt "Treppen" raus, behält Streifen)
    # anisotrop: mehr in X als in Y
    if post_sigma_x or post_sigma_y:
        blurred = cv2.GaussianBlur(
            blurred, (0, 0),
            sigmaX=float(post_sigma_x),
            sigmaY=float(post_sigma_y)
        )

    return blurred
