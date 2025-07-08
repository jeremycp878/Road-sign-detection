# 🚦 Traffic Sign Recognition & Mapping Web App

This project detects and maps traffic signs from dashcam videos using deep learning. A CNN model classifies signs in each frame, then maps detections with simulated or real GPS coordinates.

## Features
- Detects 43 GTSRB traffic sign classes
- Assigns geo-coordinates to each detection
- Interactive Leaflet map frontend with filter options
- Real-time backend API using Flask
- MongoDB stores all detections

## Tech Stack
- **Frontend:** React + Leaflet.js
- **Backend:** Flask + Python + TensorFlow
- **Database:** MongoDB (local or cloud)

## How It Works
1. A dashcam video is passed through the `send_frame.py` simulator
2. Each frame is classified using the trained CNN model
3. Detections (sign label, confidence, GPS) are sent to the Flask API
4. Flask saves data to MongoDB
5. The React frontend fetches this data and renders it on a map

## Installation

```bash
git clone https://github.com/yourusername/traffic-sign-mapping.git
cd traffic-sign-mapping
# Backend setup
cd model-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
npm run dev
