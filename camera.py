import cv2
import time

# The URL for the RTSP stream
# url = "rtsp://admin:123456@192.168.1.100:554/stream2"  # Replace with your camera's RTSP stream URL
url = "rtsp://192.168.1.100:554/stream2"  # Replace with your camera's RTSP stream URL

# Create a VideoCapture object    
cap = cv2.VideoCapture(url)

# Check if the connection was successful
if not cap.isOpened():
    print("Failed to open RTSP stream.")
else:
    while True:
        start_time = time.time()      

        
        # Read a frame from the stream
        ret, frame = cap.read()

        # Check if the frame was successfully captured               
        if not ret:
            print("Failed to capture frame from RTSP stream.")
            break

        # Display the frame
        cv2.imshow('IP Camera Stream', frame)

        print(time.time() - start_time)
        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the VideoCapture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
