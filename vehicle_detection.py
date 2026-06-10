from ultralytics import YOLO
import cv2

# Load YOLO model
model = YOLO("yolov8n.pt")

# Open traffic video
video = cv2.VideoCapture("videos/traffic.mp4")

while True:
    ret, frame = video.read()

    if not ret:
        break

    # Run YOLO detection
    results = model(frame)

    # Vehicle counters
    car_count = 0
    truck_count = 0
    bus_count = 0
    motorcycle_count = 0

    # Process detections
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

    # Total vehicles
    total_vehicles = (
        car_count +
        truck_count +
        bus_count +
        motorcycle_count
    )

    # Traffic density logic
    if total_vehicles <= 5:
        traffic_status = "Low Traffic"
        green_signal_time = 10
        signal_color = (0, 255, 0)   # Green

    elif total_vehicles <= 15:
        traffic_status = "Medium Traffic"
        green_signal_time = 20
        signal_color = (0, 255, 255) # Yellow

    else:
        traffic_status = "High Traffic"
        green_signal_time = 30
        signal_color = (0, 0, 255)   # Red

    # Draw detections
    annotated_frame = results[0].plot()

    # Display counts
    cv2.putText(annotated_frame, f"Cars: {car_count}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(annotated_frame, f"Trucks: {truck_count}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(annotated_frame, f"Buses: {bus_count}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(annotated_frame, f"Motorcycles: {motorcycle_count}", (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(annotated_frame, f"Total Vehicles: {total_vehicles}", (20, 220),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.putText(annotated_frame, f"Traffic Status: {traffic_status}", (20, 270),
                cv2.FONT_HERSHEY_SIMPLEX, 1, signal_color, 3)

    cv2.putText(annotated_frame, f"Green Signal Time: {green_signal_time} sec", (20, 320),
                cv2.FONT_HERSHEY_SIMPLEX, 1, signal_color, 3)

    # Draw traffic signal circle
    cv2.circle(annotated_frame, (600, 80), 30, signal_color, -1)

    # Show output
    cv2.imshow("AI Smart Traffic Management", annotated_frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()