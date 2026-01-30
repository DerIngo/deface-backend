import os
import urllib.request

from deface.common.config import FOLDER_CONFIG

# Ordner für Testbilder erstellen
os.makedirs(f"{FOLDER_CONFIG['upload']}/test_samples", exist_ok=True)

# Eine Liste mit verschiedenen Szenarien (Porträt, Gruppe, Profil)
test_images = {
    "einzel_portraet": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=600",
    "gruppe_business": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800",
    "profil_ansicht": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=600",
    "viele_gesichter": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800",
    "person_mit_hut": "https://images.unsplash.com/photo-1521119989659-a83eee488004?w=600"
}

def download_samples(samples):
    for name, url in samples.items():
        path = f"{FOLDER_CONFIG['upload']}/test_samples/{name}.jpg"
        urllib.request.urlretrieve(url, path)
        print(f"Erfolgreich geladen: {path}")

# Bilder herunterladen
download_samples(test_images)