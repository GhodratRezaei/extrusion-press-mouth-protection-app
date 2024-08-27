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



##########################################################################

# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QInputDialog, QMessageBox

# class PasswordPopupApp(QWidget):
#     def __init__(self):
#         super().__init__()
        
#         # Set up the window
#         self.setWindowTitle("Password Popup Example")
#         self.setGeometry(100, 100, 300, 100)
        
#         # Create a QVBoxLayout
#         layout = QVBoxLayout()
        
#         # Create a QCheckBox
#         self.checkbox = QCheckBox("Check to enter password")
#         layout.addWidget(self.checkbox)
        
#         # Connect the checkbox stateChanged signal to the slot
#         self.checkbox.stateChanged.connect(self.show_password_dialog)
        
#         # Set the layout
#         self.setLayout(layout)
    
#     def show_password_dialog(self, state):
#         if state == 2:  # Checkbox is checked
#             # Show a password input dialog
#             password, ok = QInputDialog.getText(self, "Enter Password", "Password:", echo=QLineEdit.Password)
            
#             if ok and password:
#                 QMessageBox.information(self, "Password Entered", "Password accepted.")
#             else:
#                 # Uncheck the checkbox if no password is entered or dialog is cancelled
#                 self.checkbox.setChecked(False)
#         else:
#             QMessageBox.information(self, "Checkbox Unchecked", "Checkbox was unchecked.")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
    
#     # Create an instance of the application window
#     window = PasswordPopupApp()
    
#     # Show the window
#     window.show()
    
#     # Run the application's event loop
#     sys.exit(app.exec_())


##########################################################################


# from pylogix import LogixDriver

# plc_ip_address = "192.168.1.10"
# tag_name = "YourTagName"

# plc = None
# try:
#     plc = LogixDriver(plc_ip_address)
#     plc.__enter__()  # Explicitly enter the context
#     result = plc.read(tag_name)
#     if result.Status == 'Success':
#         print(f"Tag Value: {result.Value}")
#     else:
#         print(f"Failed to read the tag. Status: {result.Status}")
# finally:
#     if plc:
#         plc.__exit__(None, None, None)  # Ensure resources are released
