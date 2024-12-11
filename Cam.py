import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('HA_1.1.pt')

# Initialize the video capture from the webcam (0 for default webcam)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

# Confidence threshold
confidence_threshold = 0.60

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Perform detection
    results = model(frame)

    # Draw results on the frame
    for result in results:
        # Results are typically returned as a list of detections
        for det in result.boxes:
            confidence = det.conf[0]  # Confidence score
            if confidence >= confidence_threshold:
                x1, y1, x2, y2 = det.xyxy[0]  # Bounding box coordinates
                class_id = int(det.cls[0])  # Class ID

                # Draw the bounding box
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

                # Draw the label
                label = f'{model.names[class_id]} {confidence:.2f}'
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # print label name
    print(model.names[class_id])
    
    
    # Display the resulting frame
    cv2.imshow('Real-time Detection, Press q to stop', frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
