from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# Allow all origins for now, you might want to restrict this in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    This endpoint accepts an image file and returns a placeholder prediction.
    In a real application, you would load your trained model and use it to
    make a prediction on the uploaded image.
    """
    # Placeholder logic: randomly return a tumor type
    tumor_types = ["glioma", "meningioma", "notumor", "pituitary"]
    prediction = random.choice(tumor_types)
    
    # You can access the file content like this:
    # contents = await file.read()
    
    return {"prediction": prediction, "filename": file.filename}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Brain Tumor Detection API"}

