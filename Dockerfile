FROM python:3.11-slim

# Systemabhängigkeiten
RUN apt update && apt upgrade -y && apt install -y \
    libgl1 \
    libglx-mesa0 \
    libglib2.0-0 \
    libxcb1 \
    libxcb-shm0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-randr0 \
    libxcb-shape0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Erst Requirements kopieren (besseres Caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Den Code kopieren
COPY deface/ /app/deface/
COPY .env.example /app/.env

# Umgebungsvariablen
ENV OPENCV_HEADLESS=1
ENV YOLO_CONFIG_DIR=/app
# Sicherstellen, dass /app im Python-Pfad ist
ENV PYTHONPATH=/app

# Testlauf
RUN python -c "import cv2; print('OpenCV geladen')"

# Der entscheidende Befehl mit Host 0.0.0.0
CMD ["uvicorn", "deface.api.deface:app", "--host", "0.0.0.0", "--port", "8000"]
