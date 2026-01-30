import cv2
import numpy as np

def paste_ellipse_hard(img, roi, filtered_roi, 
                       x1, y1, x2, y2,
                       w, h):
  # 1. Zentrum und Achsen der Ellipse berechnen
  center = (x1 + w // 2, y1 + h // 2)
  axes = (w // 2, h // 2)
  
  # 3. Eine elliptische Maske erstellen
  # Wir erstellen ein schwarzes Bild in der Größe der Box
  mask = np.zeros((h, w), dtype=np.uint8)
  # Zeichnen eine weiße gefüllte Ellipse auf die Maske
  cv2.ellipse(mask, (w // 2, h // 2), axes, 0, 0, 360, 255, -1)
  
  # 4. Maske nutzen, um nur die Ellipse ins Original zu übertragen
  # Wo die Maske weiß (255) ist, nehmen wir das verschwommene Bild
  # Wo sie schwarz (0) ist, behalten wir das Originalbild
  mask_inv = cv2.bitwise_not(mask)
  
  # Hintergrund (Original ohne Ellipse)
  bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
  # Vordergrund (Verschwommene Ellipse)
  fg = cv2.bitwise_and(filtered_roi, filtered_roi, mask=mask)
  
  # Zusammenfügen und zurück ins Originalbild kopieren
  img[y1:y2, x1:x2] = cv2.add(bg, fg)
  
  # Optional: Eine dünne weiße Linie um die Ellipse (für den Test-Look)
  # cv2.ellipse(img, center, axes, 0, 0, 360, (255, 255, 255), 1)

  return img


def paste_ellipse_feathered(img, roi, filtered_roi, x1, y1, x2, y2,
                            feather_sigma=12,
                            axes_scale=(1.0, 1.0),
                            clamp_axes=True):
    """
    Blendet filtered_roi innerhalb einer elliptischen Maske weich in das Original ein.

    img           : Originalbild (wird in-place verändert)
    roi           : Original-ROI aus img[y1:y2, x1:x2]
    filtered_roi  : gefilterte ROI (gleiche Größe wie roi)
    x1,y1,x2,y2   : ROI-Koordinaten im Originalbild
    feather_sigma : Stärke des weichen Übergangs (größer = weicher)
    axes_scale    : Ellipse etwas kleiner/größer machen, z.B. (0.95, 0.90)
    clamp_axes    : Achsen auf sinnvolle Werte begrenzen
    """

    if roi is None or filtered_roi is None or roi.size == 0 or filtered_roi.size == 0:
        return img

    h, w = roi.shape[:2]

    # Ellipsenachsen (Halbachsen)
    ax = int((w / 2) * float(axes_scale[0]))
    ay = int((h / 2) * float(axes_scale[1]))

    if clamp_axes:
        ax = max(1, min(ax, w // 2))
        ay = max(1, min(ay, h // 2))

    # 1) Binäre Ellipsenmaske
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.ellipse(mask, (w // 2, h // 2), (ax, ay), 0, 0, 360, 255, -1)

    # 2) Feather: aus harter Kante wird weicher Übergang
    # sigma=0 => keine Weichzeichnung, daher Mindestwert erzwingen
    feather_sigma = float(max(0.1, feather_sigma))
    soft = cv2.GaussianBlur(mask, (0, 0), sigmaX=feather_sigma, sigmaY=feather_sigma)

    # 3) Alpha in [0..1] + auf 3 Kanäle bringen
    alpha = (soft.astype(np.float32) / 255.0)[..., None]

    # 4) Blend
    blended = (roi.astype(np.float32) * (1.0 - alpha) +
               filtered_roi.astype(np.float32) * alpha).astype(np.uint8)

    img[y1:y2, x1:x2] = blended
    return img
