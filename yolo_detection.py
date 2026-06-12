<<<<<<< HEAD
from ultralytics import YOLO
import cv2

# Load pretrained YOLO model
model = YOLO("yolov8n.pt")

# Open video
cap = cv2.VideoCapture("traffic.mp4")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Run YOLO detection
    results = model(frame)

    # Draw results on frame
    annotated_frame = results[0].plot()

    # Show output
    cv2.imshow("YOLO Vehicle Detection", annotated_frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


=======
from ultralytics import YOLO
import cv2

# Load pretrained YOLO model
model = YOLO("yolov8n.pt")

# Open video
cap = cv2.VideoCapture("traffic.mp4")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Run YOLO detection
    results = model(frame)

    # Draw results on frame
    annotated_frame = results[0].plot()

    # Show output
    cv2.imshow("YOLO Vehicle Detection", annotated_frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


>>>>>>> e90c359cbccb63163a5ccb37c71946e6e322fc7c
