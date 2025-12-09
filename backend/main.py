from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json
import os

app = FastAPI()

# Allow all origins for now, you might want to restrict this in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and class indices
model = None
class_names = None

@app.on_event("startup")
async def load_model():
    """Load the trained model and class indices on startup"""
    global model, class_names
    
    try:
        # Load the model
        model_path = os.path.join(os.path.dirname(__file__), "tumor_detection_model.keras")
        print(f"Loading model from {model_path}...")
        model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully!")
        
        # Load class indices
        class_indices_path = os.path.join(os.path.dirname(__file__), "class_indices.json")
        print(f"Loading class indices from {class_indices_path}...")
        with open(class_indices_path, 'r') as f:
            class_indices = json.load(f)
        
        # Create reverse mapping (index -> class name)
        class_names = {v: k for k, v in class_indices.items()}
        print(f"Class names loaded: {class_names}")
        
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Preprocess the uploaded image for model prediction
    """
    # Open image from bytes
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize to model input size
    image = image.resize((224, 224))
    
    # Convert to numpy array and normalize
    image_array = np.array(image)
    image_array = image_array / 255.0
    
    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)
    
    return image_array

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    This endpoint accepts an image file and returns a tumor type prediction.
    The model predicts one of four classes: glioma, meningioma, notumor, or pituitary.
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image file
        contents = await file.read()
        
        # Preprocess image
        processed_image = preprocess_image(contents)
        
        # Make prediction
        predictions = model.predict(processed_image, verbose=0)
        
        # Get predicted class index and confidence
        predicted_class_idx = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_class_idx])
        
        # Get class name
        predicted_class = class_names[predicted_class_idx]
        
        # Get all class probabilities
        class_probabilities = {
            class_names[i]: float(predictions[0][i])
            for i in range(len(class_names))
        }
        
        return {
            "prediction": predicted_class,
            "confidence": confidence,
            "probabilities": class_probabilities,
            "filename": file.filename
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Brain Tumor Detection API"}

