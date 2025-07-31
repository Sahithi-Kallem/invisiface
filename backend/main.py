from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
from PIL import Image
import face_recognition
import io
import base64
from typing import Dict, Any
import logging
from face_cloaker import FaceCloaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="InvisiFace API", description="Face Anonymizer and Digital Identity Protection System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize face cloaker
face_cloaker = FaceCloaker()

@app.get("/")
async def root():
    return {"message": "InvisiFace API - Face Anonymizer and Digital Identity Protection System"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "InvisiFace API"}

@app.post("/api/cloak-image")
async def cloak_image(file: UploadFile = File(...)):
    """
    Apply face cloaking to an uploaded image.
    Returns the cloaked image as base64 encoded string.
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read the uploaded image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert PIL image to numpy array
        image_array = np.array(image)
        
        # Apply face cloaking
        cloaked_image_array = face_cloaker.cloak_image(image_array)
        
        # Convert back to PIL Image
        cloaked_image = Image.fromarray(cloaked_image_array)
        
        # Convert to base64 for response
        buffered = io.BytesIO()
        cloaked_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return {
            "success": True,
            "cloaked_image": f"data:image/png;base64,{img_str}",
            "message": "Image successfully cloaked"
        }
        
    except Exception as e:
        logger.error(f"Error cloaking image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/api/check-protection")
async def check_protection(file: UploadFile = File(...)):
    """
    Check if an image is protected against face recognition.
    Returns protection status and confidence scores.
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read the uploaded image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert PIL image to numpy array
        image_array = np.array(image)
        
        # Check face recognition
        protection_result = face_cloaker.check_face_recognition(image_array)
        
        return {
            "success": True,
            "is_protected": protection_result["is_protected"],
            "faces_detected": protection_result["faces_detected"],
            "confidence_scores": protection_result["confidence_scores"],
            "protection_level": protection_result["protection_level"],
            "message": protection_result["message"]
        }
        
    except Exception as e:
        logger.error(f"Error checking protection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error checking protection: {str(e)}")

@app.post("/api/download-cloaked")
async def download_cloaked_image(file: UploadFile = File(...)):
    """
    Process and return a cloaked image for download.
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read the uploaded image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert PIL image to numpy array
        image_array = np.array(image)
        
        # Apply face cloaking
        cloaked_image_array = face_cloaker.cloak_image(image_array)
        
        # Convert back to PIL Image
        cloaked_image = Image.fromarray(cloaked_image_array)
        
        # Prepare for download
        buffered = io.BytesIO()
        cloaked_image.save(buffered, format="PNG")
        buffered.seek(0)
        
        return StreamingResponse(
            io.BytesIO(buffered.getvalue()),
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=cloaked_image.png"}
        )
        
    except Exception as e:
        logger.error(f"Error preparing download: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error preparing download: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)