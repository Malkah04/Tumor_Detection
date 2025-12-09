"""
Script to train the brain tumor classification model and save it
"""
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import json

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

print("TensorFlow version:", tf.__version__)

# Data generators
train_gen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_data = train_gen.flow_from_directory(
    "data/train",
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical",
    subset="training",
    shuffle=True,
    seed=42
)

val_data = train_gen.flow_from_directory(
    "data/train",
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical",
    subset="validation",
    shuffle=False,
    seed=42
)

test_gen = ImageDataGenerator(rescale=1./255)

test_data = test_gen.flow_from_directory(
    "data/test",
    target_size=(224, 224),
    batch_size=32,
    class_mode="categorical",
    shuffle=False
)

print("\nClass indices:", train_data.class_indices)
print("Number of training samples:", train_data.samples)
print("Number of validation samples:", val_data.samples)
print("Number of test samples:", test_data.samples)

# Build model
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
    tf.keras.layers.Dense(len(train_data.class_indices), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

print("\nModel summary:")
model.summary()

# Early stopping callback
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=10,
    restore_best_weights=True
)

# Train the model
print("\nStarting training...")
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=30,
    callbacks=[early_stop],
    verbose=1
)

# Evaluate on test set
print("\nEvaluating on test set...")
test_loss, test_acc = model.evaluate(test_data)
print(f"Test Accuracy: {test_acc * 100:.2f}%")
print(f"Test Loss: {test_loss:.4f}")

# Save the model
model_path = "backend/tumor_detection_model.keras"
print(f"\nSaving model to {model_path}...")
model.save(model_path)

# Save class indices for later use
class_indices_path = "backend/class_indices.json"
print(f"Saving class indices to {class_indices_path}...")
with open(class_indices_path, 'w') as f:
    json.dump(train_data.class_indices, f, indent=2)

print("\nTraining complete!")
print(f"Model saved to: {model_path}")
print(f"Class indices saved to: {class_indices_path}")
