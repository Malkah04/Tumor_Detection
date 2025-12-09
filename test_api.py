"""
Simple script to test the Tumor Detection API
"""
import requests
import json
import os
import sys

# API endpoint
API_URL = "http://localhost:8000"

def test_root():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{API_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def test_prediction(image_path, expected_class=None):
    """Test the prediction endpoint with an image"""
    print(f"Testing prediction with: {image_path}")
    
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}\n")
        return False
    
    with open(image_path, 'rb') as f:
        files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
        response = requests.post(f"{API_URL}/predict", files=files)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Filename: {result['filename']}")
        print(f"Prediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']:.4f}")
        print("Probabilities:")
        for class_name, prob in result['probabilities'].items():
            marker = " <--" if class_name == result['prediction'] else ""
            print(f"  {class_name}: {prob:.4f}{marker}")
        
        if expected_class:
            match = result['prediction'] == expected_class
            print(f"Expected: {expected_class}, Got: {result['prediction']} - {'✓' if match else '✗'}")
        print()
        return True
    else:
        print(f"Error: {response.text}\n")
        return False

def main():
    print("=" * 60)
    print("Brain Tumor Detection API Test")
    print("=" * 60)
    print()
    
    # Test root endpoint
    if not test_root():
        print("Root endpoint test failed!")
        sys.exit(1)
    
    # Test with sample images from each class
    test_images = [
        ("data/test/glioma/Te-glTr_0000.jpg", "glioma"),
        ("data/test/meningioma/Te-meTr_0000.jpg", "meningioma"),
        ("data/test/notumor/Te-noTr_0000.jpg", "notumor"),
        ("data/test/pituitary/Te-piTr_0000.jpg", "pituitary"),
    ]
    
    success_count = 0
    for image_path, expected_class in test_images:
        if test_prediction(image_path, expected_class):
            success_count += 1
    
    print("=" * 60)
    print(f"Tests completed: {success_count}/{len(test_images)} successful")
    print("=" * 60)
    print("\nNOTE: The model has initialized weights and is not trained.")
    print("Predictions are based on random weights, so accuracy will be low (~25%).")
    print("To train the model properly, run: python3 train_and_save_model.py")

if __name__ == "__main__":
    main()
