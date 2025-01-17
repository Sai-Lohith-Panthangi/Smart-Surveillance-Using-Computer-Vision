import cv2
from datetime import datetime

def record():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(f'recordings/{datetime.now().strftime("%H-%M-%S")}.avi', fourcc, 20.0, (640, 480))
    
    while True:
        _, frame = cap.read()
        
        # Put current timestamp on the frame
        cv2.putText(frame, f'{datetime.now().strftime("%D-%H-%M-%S")}', 
                    (50, 50), cv2.FONT_HERSHEY_COMPLEX, 
                    0.6, (255, 255, 255), 2)
        
        out.write(frame)
        cv2.imshow("esc. to stop", frame)
        
        if cv2.waitKey(1) == 27:  # Exit on 'Esc' key
            cap.release()
            out.release()  # Release the video writer
            cv2.destroyAllWindows()
            break
