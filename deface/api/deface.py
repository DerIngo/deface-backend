from enum import Enum
import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import numpy as np
import cv2
from deface.anonymize import anonymize, anonymizeImage
from deface.common.config import APP_ROOT_PATH, CORS_CONFIG


class FilterType(str, Enum):
    blur = "blur"
    pixelate = "pixelate"
    line_mosaic = "line_mosaic"
    facet_effect = "facet_effect"
    verwischung_1 = "verwischung_1"

class PasteType(str, Enum):
    feathered = "feathered"
    hard = "hard"

app = FastAPI(root_path=APP_ROOT_PATH)

if CORS_CONFIG["allow_origins"]:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_CONFIG["allow_origins"],
        allow_methods=CORS_CONFIG["allow_methods"],
        allow_headers=CORS_CONFIG["allow_headers"],
        allow_credentials=CORS_CONFIG["allow_credentials"],
    )


@app.post("/deface-filename")
async def deface_filename(input_file_name: str, filter_name: FilterType, paste_ellipse_name: PasteType):
    result_path = anonymize(input_file_name, filter_name, paste_ellipse_name)
    return {"result_path": result_path}


@app.post("/deface-image")
async def deface_image(filter_name: FilterType, paste_ellipse_name: PasteType, input_file: UploadFile = File(...)):
    # 1. Byte-Stream vom Upload lesen
    contents = await input_file.read()
    
    # 2. In OpenCV Bild umwandeln
    nparr = np.frombuffer(contents, np.uint8)
    input_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if input_image is None:
        raise HTTPException(status_code=400, detail="Ungültiges Bildformat")
    # 3. Bild anonymisieren
    result_image = anonymizeImage(input_image, filter_name, paste_ellipse_name)

    # 4. Das fertige Bild in einen Buffer kodieren
    _, encoded_img = cv2.imencode('.jpg', result_image)
    
    # 5. Als Stream zurücksenden
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/jpeg")
