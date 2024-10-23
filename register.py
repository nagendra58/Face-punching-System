import cv2
import numpy as np
from IPython.display import display, clear_output
from PIL import Image
import os
import time

def register_employee():
    # Get employee details from input
    employee_id = input("Enter Employee ID: ")
    employee_name = input("Enter Employee Name: ")
    
    # Create the directory to save employee images if it doesn't exist
    if not os.path.exists('employee_faces'):
        os.makedirs('employee_faces')
    
    # Open the webcam
    video_capture = cv2.VideoCapture(0)  # 0 is the default webcam
    
    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return
    
    print(f"Capturing face for {employee_name} (ID: {employee_id})... Image will be saved in 5 seconds.")
    
    start_time = time.time()  # Record the start time
    
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        
        if not ret:
            print("Failed to capture image.")
            break
        
        # Convert the frame to RGB (OpenCV uses BGR by default)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert the frame to a PIL image for display in Jupyter Notebook
        img_pil = Image.fromarray(frame_rgb)
        
        # Display the frame in the notebook
        clear_output(wait=True)  # Clear previous frames
        display(img_pil)  # Display current frame
        
        # Check if 5 seconds have passed
        if time.time() - start_time > 5:
            # Save the current frame as the employee's image
            image_path = f"employee_faces/{employee_id}_{employee_name}.jpg"
            cv2.imwrite(image_path, frame)  # Save the image in the 'employee_faces' directory
            print(f"Image saved at {image_path}")
            break
    
    # Release the webcam
    video_capture.release()

# Call the function to start registration
register_employee()