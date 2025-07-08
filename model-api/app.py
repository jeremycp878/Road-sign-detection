from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import io

app = Flask(__name__)
model = load_model('../training/traffic_sign_model.h5')
label_map = {
    0: 'Speed Limit 20',
    1: 'Speed Limit 30',
    2: 'Speed Limit 50',
    3: 'Speed Limit 60',
    4: 'Speed Limit 70',
    5: 'Speed Limit 80',
    6: 'End of Speed Limit 80',
    7: 'Speed Limit 100',
    8: 'Speed Limit 120',
    9: 'No Passing',
    10: 'No Passing for Vehicles > 3.5 Tons',
    11: 'Right-of-Way at Intersection',
    12: 'Priority Road',
    13: 'Yield',
    14: 'Stop',
    15: 'No Vehicles',
    16: 'Vehicles > 3.5 Tons Prohibited',
    17: 'No Entry',
    18: 'General Caution',
    19: 'Dangerous Curve Left',
    20: 'Dangerous Curve Right',
    21: 'Double Curve',
    22: 'Bumpy Road',
    23: 'Slippery Road',
    24: 'Road Narrows on Right',
    25: 'Road Work',
    26: 'Traffic Signals',
    27: 'Pedestrians',
    28: 'Children Crossing',
    29: 'Bicycles Crossing',
    30: 'Beware of Ice/Snow',
    31: 'Wild Animals Crossing',
    32: 'End of All Restrictions',
    33: 'Turn Right Ahead',
    34: 'Turn Left Ahead',
    35: 'Ahead Only',
    36: 'Go Straight or Right',
    37: 'Go Straight or Left',
    38: 'Keep Right',
    39: 'Keep Left',
    40: 'Roundabout Mandatory',
    41: 'End of No Passing',
    42: 'End of No Passing for Vehicles > 3.5 Tons'
}


@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['image']
        in_memory = io.BytesIO()
        file.save(in_memory)
        data = np.frombuffer(in_memory.getvalue(), dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (32, 32)) / 255.0
        img = np.expand_dims(img, axis=0)
        pred = model.predict(img)[0]
        idx = int(np.argmax(pred))
        confidence = float(pred[idx])
        label = label_map.get(idx, f"Class {idx}")
        return jsonify({ 'sign': label, 'confidence': confidence })
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500

if __name__ == '__main__':
    app.run(port=8000)