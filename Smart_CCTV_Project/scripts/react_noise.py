import cv2  

# Global variables for rectangle coordinates and state
donel = False 
doner = False 
x1, y1, x2, y2 = 0, 0, 0, 0 

def select(event, x, y, flags, param): 
    global x1, x2, y1, y2, donel, doner 
    if event == cv2.EVENT_LBUTTONDOWN: 
        if not donel:  # First click (top-left corner)
            x1, y1 = x, y
            donel = True
        elif donel and not doner:  # Second click (bottom-right corner)
            x2, y2 = x, y
            doner = True
    print(doner, donel)

def react_noise(): 
    global x1, x2, y1, y2, donel, doner 
    cap = cv2.VideoCapture(0) 
    cv2.namedWindow("select_region") 
    cv2.setMouseCallback("select_region", select) 
    
    # First loop for selecting the region
    while True: 
        ret, frame = cap.read() 
        if not ret:
            print("Error: Unable to capture video")
            break
        
        cv2.imshow("select_region", frame) 
        if cv2.waitKey(1) == 27 or doner:  # Exit if ESC is pressed or region is selected
            cv2.destroyAllWindows() 
            if donel and doner and x1 < x2 and y1 < y2:  # Ensure valid region
                print(f"Region selected: ({x1}, {y1}) to ({x2}, {y2})")
            else:
                print("Invalid region selection. Exiting.")
                return
            break 
    
    # Second loop for motion detection
    prev_frame = None
    
    while True: 
        ret, frame = cap.read() 
        if not ret:
            print("Error: Unable to capture video")
            break
        
        # Extract the selected region from the current frame
        frame_only = frame[y1:y2, x1:x2]
        
        if prev_frame is None:
            prev_frame = frame_only
            continue
        
        # Calculate the absolute difference
        diff = cv2.absdiff(frame_only, prev_frame) 
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) 
        diff = cv2.blur(diff, (5, 5)) 
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY) 
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        
        if len(contours) > 0: 
            max_cnt = max(contours, key=cv2.contourArea) 
            x, y, w, h = cv2.boundingRect(max_cnt) 
            cv2.rectangle(frame, (x + x1, y + y1), (x + w + x1, y + h + y1), (0, 255, 0), 2) 
            cv2.putText(frame, "MOTION", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2) 
        else: 
            cv2.putText(frame, "NO-MOTION", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2) 
        
        # Draw the selected rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1) 
        cv2.imshow("esc. to exit", frame) 
        
        prev_frame = frame_only
        
        if cv2.waitKey(1) == 27:  # Exit if ESC is pressed
            break
    
    cap.release() 
    cv2.destroyAllWindows() 

# To run the function
if __name__ == "__main__":
    react_noise()
