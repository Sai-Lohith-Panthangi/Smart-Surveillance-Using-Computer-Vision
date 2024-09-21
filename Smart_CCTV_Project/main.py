import tkinter as tk
import tkinter.font as font
from scripts.motion import noise
from scripts.react_noise import react_noise
from scripts.record import record
from scripts.find_motion import find_motion
from scripts.identify import maincall
from scripts.in_out import in_out
from PIL import Image, ImageTk


# Create the main window
window = tk.Tk()
window.title("Smart CCTV")
window.iconphoto(False, tk.PhotoImage(file='mn.png'))
window.geometry('1080x700')

# Create a frame to hold widgets
frame1 = tk.Frame(window)

# Title label
label_title = tk.Label(frame1, text="Smart CCTV Camera")
label_font = font.Font(size=35, weight='bold', family='Helvetica')
label_title['font'] = label_font
label_title.grid(pady=(10, 10), column=2)

# Load and resize icons
def load_image(path, size=(50, 50)):
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

icon = load_image('icons/spy.png', (150, 150))
label_icon = tk.Label(frame1, image=icon)
label_icon.grid(row=1, pady=(5, 10), column=2)

# Button images
btn1_image = load_image('icons/lamp.png')
btn2_image = load_image('icons/rectangle-of-cutted-line-geometricalshape.png')
btn3_image = load_image('icons/security-camera.png')
btn4_image = load_image('icons/recording.png')
btn5_image = load_image('icons/exit.png')
btn6_image = load_image('icons/incognito.png')
btn7_image = load_image('icons/recording.png')

# --------------- Buttons -------------------#
btn_font = font.Font(size=25)

btn1 = tk.Button(frame1, text='Monitor', height=90, width=180, fg='green',
                 command=find_motion, image=btn1_image, compound='left')
btn1['font'] = btn_font
btn1.grid(row=3, pady=(20, 10))

btn2 = tk.Button(frame1, text='Rectangle', height=90, width=180, fg='orange',
                 command=react_noise, compound='left', image=btn2_image)
btn2['font'] = btn_font
btn2.grid(row=3, pady=(20, 10), column=3, padx=(20, 5))

btn3 = tk.Button(frame1, text='Noise', height=90, width=180, fg='green',
                 command=noise, image=btn3_image, compound='left')
btn3['font'] = btn_font
btn3.grid(row=5, pady=(20, 10))

btn4 = tk.Button(frame1, text='Record', height=90, width=180, fg='orange',
                 command=record, image=btn4_image, compound='left')
btn4['font'] = btn_font
btn4.grid(row=5, pady=(20, 10), column=3)

btn6 = tk.Button(frame1, text='In Out', height=90, width=180, fg='green',
                 command=in_out, image=btn6_image, compound='left')
btn6['font'] = btn_font
btn6.grid(row=5, pady=(20, 10), column=2)

btn5 = tk.Button(frame1, text='Exit', height=90, width=180, fg='red', command=window.quit, image=btn5_image, compound='left')
btn5['font'] = btn_font
btn5.grid(row=6, pady=(20, 10), column=2)

btn7 = tk.Button(frame1, text="Identify", fg="orange", command=maincall,
                 compound='left', image=btn7_image, height=90, width=180)
btn7['font'] = btn_font
btn7.grid(row=3, column=2, pady=(20, 10))

# Pack the frame
frame1.pack()

# Run the main loop
window.mainloop()
