# Brain Tumor Detection API

A deep learning-based API for detecting brain tumor types from MRI images using a Convolutional Neural Network (CNN).

## Features

- Classifies brain MRI images into 4 categories:
  - **Glioma**
  - **Meningioma**
  - **No Tumor**
  - **Pituitary**
- Returns prediction with confidence scores and probability distribution
- RESTful API built with FastAPI
- TensorFlow/Keras-based CNN model

## Project Structure

```
.
├── backend/
│   ├── main.py                      # FastAPI application with model integration
│   ├── requirements.txt             # Python dependencies
│   ├── tumor_detection_model.keras  # Trained CNN model (43MB)
│   └── class_indices.json          # Tumor type to index mapping
├── data/
│   ├── train/                      # Training images by tumor type
│   └── test/                       # Test images by tumor type
├── train_model.ipynb               # Jupyter notebook for model exploration
├── train_and_save_model.py         # Script to train model from scratch
├── create_demo_model.py            # Script to create demo model
└── test_api.py                     # API testing script
```

## Setup

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/philopaterwaheed/Tumor_Detection.git
cd Tumor_Detection
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

## Usage

### Starting the API Server

```bash
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### GET `/`
Returns a welcome message.

**Response:**
```json
{
  "message": "Welcome to the Brain Tumor Detection API"
}
```

#### POST `/predict`
Accepts an MRI image and returns tumor classification.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: Image file (JPEG, PNG, etc.)

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -F "file=@path/to/brain_scan.jpg"
```

**Response:**
```json
{
  "prediction": "glioma",
  "confidence": 0.8542,
  "probabilities": {
    "glioma": 0.8542,
    "meningioma": 0.0734,
    "notumor": 0.0421,
    "pituitary": 0.0303
  },
  "filename": "brain_scan.jpg"
}
```

### Testing the API

Run the test script to verify the API is working:

```bash
python3 test_api.py
```

This will test the API with sample images from each tumor class.

### Using Python Requests

```python
import requests

# Test the API
url = "http://localhost:8000/predict"
files = {'file': open('path/to/image.jpg', 'rb')}
response = requests.post(url, files=files)

result = response.json()
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")
```

## Model Information

### Architecture

The model is a Convolutional Neural Network (CNN) with the following architecture:
- 3 Convolutional blocks (Conv2D + MaxPooling2D)
- Fully connected layers with dropout
- Softmax output layer for 4 classes

**Total parameters:** 11,169,476 (~43 MB)

### Training

To train the model with your data:

```bash
python3 train_and_save_model.py
```

This will:
1. Load training data from `data/train/`
2. Train the CNN model
3. Evaluate on test data from `data/test/`
4. Save the trained model to `backend/tumor_detection_model.keras`

**Note:** Training can take significant time depending on your hardware (GPU recommended).

### Model Performance

The current model uses initialized weights. For production use, train the model with:
- More epochs
- Data augmentation
- Transfer learning (e.g., ResNet, VGG)

Expected performance after proper training:
- Training accuracy: 90%+
- Validation accuracy: 85%+
- Test accuracy: 80%+

## Dataset

The dataset should be organized as follows:

```
data/
├── train/
│   ├── glioma/
│   ├── meningioma/
│   ├── notumor/
│   └── pituitary/
└── test/
    ├── glioma/
    ├── meningioma/
    ├── notumor/
    └── pituitary/
```

Each subdirectory should contain MRI images for that class.

## API Documentation

Once the server is running, access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Dependencies

### Backend
- FastAPI: Web framework
- TensorFlow: Deep learning model
- Pillow: Image processing
- NumPy: Numerical operations
- Uvicorn: ASGI server

See `backend/requirements.txt` for complete list.

## Development

### Running in Development Mode

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-restart on code changes.

## Notes

- The model expects 224x224 RGB images
- Images are automatically resized and normalized
- All image formats supported by Pillow are accepted
- GPU acceleration is used if available (CUDA)

## Future Improvements

- [ ] Train model with full dataset for better accuracy
- [ ] Implement model versioning
- [ ] Add batch prediction endpoint
- [ ] Include confidence thresholds
- [ ] Add image preprocessing validation
- [ ] Implement model explainability (e.g., Grad-CAM)
- [ ] Add authentication for production use

## License

This project is open source and available under the MIT License.

## Contact

For questions or issues, please open an issue on GitHub.
