import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import threading

class PeterplugBlurApp:
    def __init__(self, root):
        self.root = root
        self.root.title("peterplug blur app")
        self.root.geometry("560x145")
        self.root.resizable(False, False)  # make the window non-resizable
        self.input_file = None
        self.process = None
        self.frame_rate = tk.StringVar()
        self.frame_rate.set("24")  # default value
        self.resolution = tk.StringVar()
        self.resolution.set("1920x1080")  # default value
        
        # create frame for buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)

        # create input file label and entry
        self.input_label = tk.Label(self.button_frame, text="Input File:")
        self.input_label.grid(row=0, column=0, padx=5)

        self.input_entry = tk.Entry(self.button_frame, width=55)
        self.input_entry.grid(row=0, column=1, padx=5)

        # create select file button
        self.select_button = tk.Button(self.button_frame, text="Browse", command=self.select_input_file)
        self.select_button.grid(row=0, column=2, padx=5)

        # create frame rate label and dropdown
        self.frame_rate_label = tk.Label(self.button_frame, text="Res/FPS:")
        self.frame_rate_label.grid(row=1, column=0, padx=5)

        self.frame_rate_dropdown = tk.OptionMenu(self.button_frame, self.frame_rate, "24", "30", "60")
        self.frame_rate_dropdown.grid(row=1, column=2, padx=5)

        self.resolution_dropdown = tk.OptionMenu(self.button_frame, self.resolution, "1280x720", "1920x1080", "2560x1440")
        self.resolution_dropdown.grid(row=1, column=1, padx=5)

        # create start button
        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_blur)
        self.start_button.grid(row=2, column=1, padx=5,pady=5)

        # create status bar
        self.status_bar = tk.Label(self.root, text="Select a file and press Start")
        self.status_bar.pack(pady=5)

        # cind the close event to the on_close method
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def select_input_file(self):
        self.input_file = filedialog.askopenfilename()
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, self.input_file)

    def start_blur(self):
        if self.input_entry.get() == "":
            print("Please select an input file")
            return

        # get the output file path
        output_file = os.path.join(os.path.dirname(self.input_entry.get()), "blur.mp4")

        # check if the output file already exists and delete it if necessary
        if os.path.exists(output_file):
            os.remove(output_file)

        # create the ffmpeg command
        command = f"ffmpeg -i {self.input_entry.get()} -vf 'scale={self.resolution.get()}, minterpolate=mi_mode=mci:mc_mode=aobmc:vsbmc=1, tblend=all_mode=average, framestep=2' -pix_fmt yuv420p -b:v 24M -r {self.frame_rate.get()} {output_file}"

        # run the ffmpeg command in a separate thread
        self.thread = threading.Thread(target=self.run_ffmpeg, args=(command, output_file))
        self.thread.start()

    def run_ffmpeg(self, command, output_file):
        self.status_bar['text'] = "Running FFmpeg..."
        self.process = subprocess.Popen(command, shell=True)
        self.process.wait()
        self.status_bar['text'] = f"FFmpeg finished. Output file created: {output_file}"

    def on_close(self):
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PeterplugBlurApp(root)
    root.mainloop()
