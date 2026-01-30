import logging

# Logging konfigurieren (Formatierung für Docker-Logs optimiert)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)