import cv2
import os
import numpy as np
import tkinter as tk
from tkinter import font, messagebox

# Ensure the 'persons' directory exists
if not os.path.exists('persons'):
    os.makedirs('persons')

# Global flag to control the identification loop
identifying = False

# Function to collect data from video feed
def collect_data():
    def submit():
        name = entry_name.get()
        ids = entry_id.get()
        if not name or not ids:
            messagebox.showerror("Input Error", "Please enter both ID and Name")
            return
        
        count = 1
        cap = cv2.VideoCapture(0)
        cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        capturing = True  # Flag to control capturing

        while capturing:
            _, frm = cap.read()
            gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(gray, 1.4, 1)

            for x, y, w, h in faces:
                cv2.rectangle(frm, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi = gray[y:y + h, x:x + w]
                
                cv2.imwrite(f"persons/{name}-{count}-{ids}.jpg", roi)
                count += 1
                cv2.putText(frm, f"{count}", (20, 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
                cv2.imshow("new", roi)

            cv2.imshow("identify", frm)

            key = cv2.waitKey(1)
            if key == 27 or count > 50:  # ESC key or limit reached
                capturing = False

        cv2.destroyAllWindows()
        cap.release()
        train(name, ids)  # Pass name and id to train

    # Create a new Tkinter window for input
    input_window = tk.Toplevel()
    input_window.title("Input Data")

    tk.Label(input_window, text="Enter ID:").pack()
    entry_id = tk.Entry(input_window)
    entry_id.pack()

    tk.Label(input_window, text="Enter Name:").pack()
    entry_name = tk.Entry(input_window)
    entry_name.pack()

    tk.Button(input_window, text="Submit", command=submit).pack()

# Function to train the recognizer
def train(name, ids):
    print("Training part initiated!")
    
    recog = cv2.face.LBPHFaceRecognizer_create()
    dataset = 'persons'
    paths = [os.path.join(dataset, im) for im in os.listdir(dataset)]

    faces = []
    ids_list = []

    for path in paths:
        ids_list.append(int(path.split('-')[2].split('.')[0]))
        faces.append(cv2.imread(path, 0))

    recog.train(faces, np.array(ids_list))
    recog.save('model.yml')

# Function to identify faces in real-time video feed
def identify():
    global identifying
    identifying = True
    cap = cv2.VideoCapture(0)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # Build label dictionary from the persons folder
    paths = [os.path.join("persons", im) for im in os.listdir("persons")]
    labelslist = {path.split('-')[2].split('.')[0]: path.split('-')[0] for path in paths}

    recog = cv2.face.LBPHFaceRecognizer_create()
    recog.read('model.yml')

    while identifying:  # Keep identifying until the window is closed
        _, frm = cap.read()
        gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, 1.3, 2)

        for x, y, w, h in faces:
            cv2.rectangle(frm, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi = gray[y:y + h, x:x + w]

            label = recog.predict(roi)

            if label[1] < 100:
                cv2.putText(frm, f"{labelslist[str(label[0])]} {int(label[1])}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            else:
                cv2.putText(frm, "unknown", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2.imshow("identify", frm)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to stop identification when the window is closed
def stop_identifying():
    global identifying
    identifying = False

# Function to create the main GUI
def maincall():
    root = tk.Tk()
    root.geometry("480x100")
    root.title("Identify")

    # Set up the Tkinter window close handler
    root.protocol("WM_DELETE_WINDOW", stop_identifying)

    label = tk.Label(root, text="Select below buttons")
    label.grid(row=0, columnspan=2)
    label_font = font.Font(size=35, weight='bold', family='Helvetica')
    label['font'] = label_font

    btn_font = font.Font(size=25)
    button1 = tk.Button(root, text="Add Member", command=collect_data, height=2, width=20)
    button1.grid(row=1, column=0, pady=(10, 10), padx=(5, 5))
    button1['font'] = btn_font

    button2 = tk.Button(root, text="Start with known", command=identify, height=2, width=20)
    button2.grid(row=1, column=1, pady=(10, 10), padx=(5, 5))
    button2['font'] = btn_font

    root.mainloop()

# Main call to initiate the GUI
if __name__ == "__main__":
    maincall()
