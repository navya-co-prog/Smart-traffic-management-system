
from flask import Flask, render_template, Response, jsonify
import cv2
from ultralytics import YOLO

app = Flask(__name__)

# Load YOLO model
model = YOLO("yolov8n.pt")

# Dashboard data
traffic_data = {                  
    "cars": 0,
    "trucks": 0,
    "buses": 0,
    "motorcycles": 0,
    "total": 0,
    "status": "Low Traffic",
    "signal_time": 10
}

def generate_frames():

    cap = cv2.VideoCapture("videos/traffic.mp4")

    while True:

        success, frame = cap.read()

        if not success:
            break

        # YOLO detection
        results = model(frame)

        # Vehicle counts
        car_count = 0
        truck_count = 0
        bus_count = 0
        motorcycle_count = 0

        for result in results:

            boxes = result.boxes
            names = result.names

            for box in boxes:

                cls = int(box.cls[0])
                label = names[cls]

                if label == "car":
                    car_count += 1

                elif label == "truck":
                    truck_count += 1

                elif label == "bus":
                    bus_count += 1

                elif label == "motorcycle":
                    motorcycle_count += 1

        total_vehicles = (
            car_count +
            truck_count +
            bus_count +
            motorcycle_count
        )
        

        # Traffic logic
        if total_vehicles <= 5:
            traffic_status = "Low Traffic"
            signal_time = 10

        elif total_vehicles <= 15:
            traffic_status = "Medium Traffic"
            signal_time = 20

        else:
            traffic_status = "High Traffic"
            signal_time = 30

        # Update dashboard
        traffic_data["cars"] = car_count
        traffic_data["trucks"] = truck_count
        traffic_data["buses"] = bus_count
        traffic_data["motorcycles"] = motorcycle_count
        traffic_data["total"] = total_vehicles
        traffic_data["status"] = traffic_status
        traffic_data["signal_time"] = signal_time

        # Draw detection boxes
        annotated_frame = results[0].plot()

        # Convert frame
        ret, buffer = cv2.imencode('.jpg', annotated_frame)

        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/video')
def video():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/data')
def data():
    return jsonify(traffic_data)

if __name__ == '__main__':

    app.run(debug=True)   