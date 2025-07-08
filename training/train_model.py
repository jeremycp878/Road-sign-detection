
import os
import numpy as np
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from glob import glob


IMG_SIZE = 32
NUM_CLASSES = 43

def load_data(data_dir):
    images = []
    labels = []
    for class_id in range(NUM_CLASSES):
        class_dir = os.path.join(data_dir, f"{class_id:05d}")
        image_files = glob(os.path.join(class_dir, '*.ppm'))
        for image_file in image_files:
            img = cv2.imread(image_file)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            images.append(img)
            labels.append(class_id)
    X = np.array(images) / 255.0
    y = to_categorical(labels, NUM_CLASSES)
    return train_test_split(X, y, test_size=0.2, random_state=42)


X_train, X_val, y_train, y_val = load_data('dataset/Train')

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    MaxPooling2D(),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(NUM_CLASSES, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=10, batch_size=64)

model.save('traffic_sign_model.h5')
