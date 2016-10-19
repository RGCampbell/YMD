import urllib.request
import urllib.parse
import re
import os
from subprocess import Popen, PIPE
import time
import pafy
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading


class Main(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        
        #starts thread for gui
        thread_1 = threading.Thread(target=self.gui, args=())
        thread_1.start()
        
    def gui(self):
        #frame with a label to store input components
        self.input_frame = tk.LabelFrame(self, text="import", padx=7, pady=6, width=200,height=200)
        self.input_frame.grid(row=0,column=0,padx=(5,4), pady=(0,5))

        #input directory entry
        self.file_input = tk.StringVar()
        self.dir_input = ttk.Entry(self.input_frame, width=54, textvariable=self.file_input)
        self.dir_input.grid(row=0, column=0, sticky='W')
        #button to change input directory
        self.dir_change_input = ttk.Button(self.input_frame, text="change", command=self.input_dir_change)
        self.dir_change_input.grid(row=0, column=1, sticky='E')

        #large entry box for input
        self.enter_input = ScrolledText(self.input_frame, width=48, height=6)
        self.enter_input.grid(row=1, column=0, columnspan=2, sticky='W')

        #frame with a label to store help components
        self.side_frame = tk.LabelFrame(self, text="Help", padx=2, pady=4, width=50, height=300)
        self.side_frame.grid(row=0, column=1, rowspan=6,padx=(0,5), pady=(0,5), sticky='NW')

        #instructions
        self.side_label_1 = tk.Label(self.side_frame, text="Step 1: Either choose a .txt file from \n a local drive or enter it. \n \n The input must be formated like the \n example shows "+"("+"caps sensitive."+")")
        self.side_label_1.grid(row=0,column=0, sticky='W')  
        self.side_label_2 = tk.Label(self.side_frame, text="e.g. Artist - Song")
        self.side_label_2.grid(row=1,column=0)
        self.side_break = tk.Label(self.side_frame, text="\n\n")
        self.side_break.grid(row=2)
        self.side_label_4 = tk.Label(self.side_frame, text="Step 2: Choose folder to put songs.")
        self.side_label_4.grid(row=3)
        self.side_label_5 = tk.Label(self.side_frame, text="Check 'sort into folders' to output \n songs into artist named sub-folders \n in a folder named 'music'.")
        self.side_label_5.grid(row=4)
    
        #frame with a label to store output components               
        self.output_frame = tk.LabelFrame(self, text="output", padx=7, pady=6,width=200,height=200)
        self.output_frame.grid(row=2, column=0, padx=(5,4), pady=(9,5), sticky='W')

        #output directory entry
        self.file_output = tk.StringVar()
        self.cwd = str(os.getcwd())
        self.dir_output = ttk.Entry(self.output_frame, width=54, textvariable=self.file_output)
        self.dir_output.grid(row=4, column=0, sticky='W')
        #sets default entry
        self.file_output.set(self.cwd)
        
        #button to change output location
        self.dir_change_output = ttk.Button(self.output_frame, text="change", command=self.output_dir_change)
        self.dir_change_output.grid(row=4, column=1, sticky='W')

        #checkbox to sort into folders
        self.checkbox_counter = 0
        self.check_sort_into = 0
        self.sort_into = tk.Checkbutton(self.output_frame, text="sort into folders", variable=self.check_sort_into, command=self.check_checkbutton)
        self.sort_into.grid(row=5, column=0, sticky='W')

        #button that executes download_start
        self.download_button = ttk.Button(self, text="download", command=self.download_start)
        self.download_button.grid(row=4, pady=(0,2))

        #error messages
        self.incorrect_input_1 = tk.Label(self, text="Please enter a valid input", fg='red')
        self.incorrect_input_2 = tk.Label(self, text="Please enter a valid output location", fg='red')
        self.no_internet = tk.Label(self, text="No internet connection detected", fg='red')

        #completed message + progressbar
        self.completed = tk.Label(self, text="completed!", fg='blue')
        self.progressbar = ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=400)

    def input_dir_change(self):
        self.incorrect_input_1.grid_remove()
        #opens file browser to choose input file
        self.text_input = filedialog.askopenfilename(filetypes = [("Text file", "*.txt")], title='Select a text file')
        self.file_input.set(self.text_input)

    def output_dir_change(self):
        self.incorrect_input_2.grid_remove()
        #opens file browser to choose input file
        self.text_output = filedialog.askdirectory()
        self.file_output.set(self.text_output)
        
    def check_checkbutton(self):
        self.checkbox_counter +=1
        #checks state of checkbox
        if self.checkbox_counter % 2 == 1:
            self.check_sort_into = 1
            #sets output entry with music
            self.check_box_add = str(self.dir_output.get()) + "\\music"
            self.file_output.set(self.check_box_add)
            
        else:
            #sets output entry without music
            self.check_box_num = int(len(str(self.dir_output.get())) - 6)
            self.check_box_take = str(self.dir_output.get())[:self.check_box_num] 
            self.file_output.set(self.check_box_take)
            self.check_sort_into = 0
    
    def download_start(self):
        def download_start_main():
            self.amount_labels = 0
            self.incorrect_input_errors = 0
            self.input_find = self.dir_input.get()
            self.input_type = self.enter_input.get('0.0', 'end').splitlines()

            #checks if input entry is empty and if it exists
            if self.input_find != "" and os.path.exists(self.input_find) == True:
                self.incorrect_input_1.grid_remove()
                with open(self.input_find, 'r+') as self.f:
                    #sets song list
                    self.lines = self.f.read().splitlines()

            #checks if input box is empty
            elif self.input_type[0]!="":
                self.incorrect_input_1.grid_remove()
                counter = 0
                for element in self.input_type:
                    #checks if any lines are over 45 chars
                    if len(element) < 45:
                        counter += 1
                        if counter == len(self.input_type):
                            self.lines = self.input_type
                    elif len(element) > 44:
                        self.incorrect_input_1.grid(row=5)
                        self.amount_labels +=1
                        self.incorrect_input_errors +=1
                        
            #displays error message
            else:
                self.incorrect_input_1.grid(row=5)
                self.amount_labels +=1
                self.incorrect_input_errors +=1

            self.output_loc = self.dir_output.get()
            #checks if output entry is empty and if it exists
            if self.dir_output.get() != "" and os.path.exists(self.dir_output.get()):
                self.incorrect_input_2.grid_remove()
                #sets song list
                self.output = self.dir_output.get()
            #displays error message
            else:
                if self.amount_labels == 1:
                    self.incorrect_input_2.grid(row=6)
                    self.amount_labels +=1
                else:
                    self.incorrect_input_2.grid(row=5)
                    self.amount_labels +=1
                self.incorrect_input_errors +=1

            #check if connected to internet
            try:
                response=urllib.request.urlopen('http://www.google.com', timeout=1)
                self.no_internet.grid_remove()
            except urllib.request.URLError as err:
                self.incorrect_input_errors +=1
                if self.amount_labels == 1:
                    self.no_internet.grid(row=6)
                elif self.amount_labels == 2:
                    self.no_internet.grid(row=7)
                else:
                    self.no_internet.grid(row=5)
                    
            #checks amount of error messages then executes main_download in a new thread
            if self.incorrect_input_errors == 0:
                thread_3 = threading.Thread(target=self.main_download, args=())
                thread_3.start()
            else:
                pass
        #starts download_start_main in a new thread
        #doing it this way means only one thread can be created at a time
        self.thread_2 = threading.Thread(target=download_start_main, args=())
        self.thread_2.start()
        
    def main_download(self):
        #greys out some of the widgets
        self.download_button.config(state="disabled")
        self.sort_into.config(state="disabled")
        self.dir_change_input.config(state="disabled")
        self.dir_change_output.config(state="disabled")

        #starts progressbar
        self.progressbar.grid(row=5)
        self.progressbar.start(35)
        for word in self.lines:
            #search function    
            query_string = urllib.parse.urlencode({"search_query" : word})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            search_1 = ("http://www.youtube.com/watch?v=" + search_results[0])
            search_2 = ("http://www.youtube.com/watch?v=" + search_results[2])
            s1 = pafy.new(search_1)
            s2 = pafy.new(search_2)

            #sets link
            if int(s1.length) <= int(s2.length) and int(s1.length) > 90:
                link = str(search_1)
            elif int(s2.length) < int(s1.length) and int(s2.length) > 90:
                link = str(search_2)
            else:
                link = str(search_1)
                    
            #downloads
            CREATE_NO_WINDOW = 0x08000000
            name = word + ".opus"
            download_com = ["cmd.exe", "/k", 'youtube-dl', "-x", "-o", str(name), str(link)]
            download = Popen(download_com, creationflags=CREATE_NO_WINDOW)
            """name = word + ".opus"
            yt_command = ("youtube-dl -x "'-o "' + name + '" ' + str(link))
            os.system(yt_command)"""

            #sets convertion directory
            if self.check_sort_into == 1:
                if os.path.isdir(str(self.output) + "\\music\\") == True:
                    pass
                else:
                    os.makedirs(str(self.output) + "\\music\\")
                pos = word.index('-') - 1
                artist = word[:pos]
                if os.path.isdir(str(self.output) + "\\music\\" + artist) == True:
                    loc_name = str(self.output) + "\\music\\" + artist + "\\" + word + ".mp3"
                else:
                    os.makedirs(str(self.output) + "\\music\\" + artist)
                    loc_name = str(self.output) + "\\music\\" + artist + "\\" + word + ".mp3"
            else:
                loc_name = str(self.output) + "\\" + word + ".mp3"

            initial_file = (str(self.output) + "\\" + str(name))

            convert_command = ["C:/Program Files (x86)/VideoLAN/VLC/vlc.exe",
                "-I", "dummy", "-vvv",
                initial_file,
                "--sout=#transcode{acodec=mpga,ab=192}:standard{access=file,dst=" + loc_name]

            #converts to mp3
            while True:
                if os.path.exists(initial_file):
                    time.sleep(2)
                    convert = Popen(convert_command)
                    break
                else:
                    pass

            time.sleep(10)
            #deletes unconverted file
            while True:
                try:
                    os.remove(initial_file)
                    convert.terminate()
                    break
                except:
                    pass
                time.sleep(2)

        #progressbar stops
        self.progressbar.stop()
        self.progressbar.grid_remove()
        self.completed.grid(row=5)
        
#first run of the program
def first_run():
    #downloads module
    os.system("pip install youtube-dl")
    print("Welcome")
    #writes a 1 to runtime
    with open("runtime.txt", 'w') as r:
        r.write("1")
    run()
#every other run of the program
def run():
    #sets tkinter parameters
    root = tk.Tk()
    root.title("Automatic Music Downloader")
    root.geometry("648x355")
    root.resizable(width=False, height=False)
    #creates object of class
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    #checks runtime of program
    if os.path.exists("runtime.txt") == False:
        with open("runtime.txt", 'w') as write_runtime:
            write_runtime.write("0")

    with open("runtime.txt", 'r+') as r:
        read = r.readlines()
        if read[0] == "1":
            run()
        else:
            first_run()
