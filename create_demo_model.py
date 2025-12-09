"""
Script to create a demo model architecture for brain tumor classification.
In production, this model would be properly trained with data.
For this demo, we're creating the architecture that matches the training notebook.
"""
import tensorflow as tf
import json
import os

print("TensorFlow version:", tf.__version__)

# Define the class labels (matching the data/train directory structure)
class_indices = {
    "glioma": 0,
    "meningioma": 1,
    "notumor": 2,
    "pituitary": 3
}

num_classes = len(class_indices)

# Build the same model architecture as in the notebook
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224,224,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print("\nModel summary:")
model.summary()

# Save the model
model_path = "backend/tumor_detection_model.keras"
print(f"\nSaving model to {model_path}...")
os.makedirs("backend", exist_ok=True)
model.save(model_path)

# Save class indices for later use
class_indices_path = "backend/class_indices.json"
print(f"Saving class indices to {class_indices_path}...")
with open(class_indices_path, 'w') as f:
    json.dump(class_indices, f, indent=2)

print("\nModel creation complete!")
print(f"Model saved to: {model_path}")
print(f"Class indices saved to: {class_indices_path}")
print("\nNOTE: This is a model with initialized weights.")
print("In production, you would train this model with your data using train_and_save_model.py")
