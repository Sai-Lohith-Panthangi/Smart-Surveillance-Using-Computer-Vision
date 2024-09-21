import cv2
import time
from skimage.metrics import structural_similarity
from datetime import datetime
import beepy
import os

def spot_diff(frame1, frame2):
    # If frame1 or frame2 is a tuple, extract the second element (the image)
    if isinstance(frame1, tuple):
        frame1 = frame1[1]
    if isinstance(frame2, tuple):
        frame2 = frame2[1]

    # Convert to grayscale
    g1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Blur the images to reduce noise
    g1 = cv2.blur(g1, (2, 2))
    g2 = cv2.blur(g2, (2, 2))

    # Compute the structural similarity index (SSIM)
    (score, diff) = structural_similarity(g2, g1, full=True)
    print("Image similarity", score)

    # Convert the diff image to uint8 format for thresholding
    diff = (diff * 255).astype("uint8")
    thresh = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY_INV)[1]

    # Find contours in the thresholded image
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    contours = [c for c in contours if cv2.contourArea(c) > 50]

    if len(contours):
        for c in contours:
            # Draw bounding box around the detected difference
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Show the result
        cv2.imshow("Difference", thresh)
        cv2.imshow("Frame", frame1)

        # Play alert sound
        beepy.beep(sound=4)

        # Ensure 'stolen' directory exists
        if not os.path.exists("stolen"):
            os.makedirs("stolen")

        # Save the image
        cv2.imwrite("stolen/" + datetime.now().strftime('%y-%m-%d_%H-%M-%S') + ".jpg", frame1)
        
        # Wait for user to close windows
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return 1
    else:
        print("No significant difference detected (nothing stolen).")
        return 0
