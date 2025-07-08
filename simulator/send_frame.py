import cv2
import requests
import json

with open('0000f77c-62c2a288.json') as f:
    gps_data = json.load(f)

video = cv2.VideoCapture('dashcam_sample.mov')
frame_num = 0
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"Total frames in video: {total_frames}")

while True:
    ret, frame = video.read()
    if not ret:
        break  
    if frame_num % 5 == 0:
        _, img_encoded = cv2.imencode('.jpg', frame)
        res = requests.post('http://localhost:8000/predict', files={'image': img_encoded.tobytes()})
        
        if res.status_code == 200:
            pred = res.json()
            coord = gps_data[frame_num // 30] 
            if pred['confidence'] > 0.7:
                detection = {
                    'sign': pred['sign'],
                    'confidence': pred['confidence'],
                    'latitude': coord['gps']['latitude'],
                    'longitude': coord['gps']['longitude']
                }
                requests.post('http://localhost:5000/detections', json=detection)
                print(f"Frame {frame_num}: Detected {pred['sign']} at ({coord['gps']['latitude']}, {coord['gps']['longitude']})")
            else:
                print(f"Frame {frame_num}: No significant detection.")
        else:
            print(f"Error in prediction request: {res.status_code}")

    frame_num += 1

video.release()
print("Finished processing dashcam video.")
