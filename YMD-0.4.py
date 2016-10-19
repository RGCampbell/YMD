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
        thread_1 = threading.Thread(target=self.gui, args=())
        thread_1.start()
        
    def gui(self):
        self.input_frame = tk.LabelFrame(self, text="import", padx=7, pady=6, width=200,height=200)
        self.input_frame.grid(row=0,column=0,padx=(5,4), pady=(0,5))

        self.file_input = tk.StringVar()
        self.dir_input = ttk.Entry(self.input_frame, width=54, textvariable=self.file_input)
        self.dir_input.grid(row=0, column=0, sticky='W')
        self.dir_change_input = ttk.Button(self.input_frame, text="change", command=self.input_dir_change)
        self.dir_change_input.grid(row=0, column=1, sticky='E')

        self.enter_input = ScrolledText(self.input_frame, width=48, height=6)
        self.enter_input.grid(row=1, column=0, columnspan=2, sticky='W')

        self.side_frame = tk.LabelFrame(self, text="Help", padx=2, pady=4, width=50, height=300)
        self.side_frame.grid(row=0, column=1, rowspan=6,padx=(0,5), pady=(0,5), sticky='NW')

        self.side_label_1 = tk.Label(self.side_frame, text="Choose a .txt file from a local drive \n or enter it instead. \n \n The input must be formated like the \n example shows "+"("+"caps sensitive."+")")
        self.side_label_1.grid(row=0,column=0, sticky='W')  
        self.side_label_2 = tk.Label(self.side_frame, text="e.g. Artist - Song")
        self.side_label_2.grid(row=1,column=0)
        self.side_break = tk.Label(self.side_frame, text="\n\n")
        self.side_break.grid(row=2)
        self.side_label_4 = tk.Label(self.side_frame, text="Choose folder to output songs to.")
        self.side_label_4.grid(row=3)
        self.side_label_5 = tk.Label(self.side_frame, text="Check 'sort into folders' to output \n songs into artist named sub-folders \n in a folder named music.")
        self.side_label_5.grid(row=4)
    
                                     
        self.output_frame = tk.LabelFrame(self, text="output", padx=7, pady=6,width=200,height=200)
        self.output_frame.grid(row=2, column=0, padx=(5,4), pady=(9,5), sticky='W')
    
        self.file_output = tk.StringVar()
        self.cwd = str(os.getcwd())
        self.dir_output = ttk.Entry(self.output_frame, width=54, textvariable=self.file_output)
        self.dir_output.grid(row=4, column=0, sticky='W')
        self.file_output.set(self.cwd)
        self.dir_change_output = ttk.Button(self.output_frame, text="change", command=self.output_dir_change)
        self.dir_change_output.grid(row=4, column=1, sticky='W')

        self.checkbox_counter = 0
        self.check_sort_into = 0
        self.sort_into = tk.Checkbutton(self.output_frame, text="sort into folders", variable=self.check_sort_into, command=self.check_checkbutton)
        self.sort_into.grid(row=5, column=0, sticky='W')

        self.download_button = ttk.Button(self, text="download", command=self.download_start)
        self.download_button.grid(row=4, pady=(0,2))
        
        self.incorrect_input_1 = tk.Label(self, text="Please enter a valid input", fg='red')
        self.incorrect_input_2 = tk.Label(self, text="Please enter a valid output location", fg='red')
        self.no_internet = tk.Label(self, text="No internet connection detected", fg='red')
        
        self.completed = tk.Label(self, text="completed!", fg='blue')
        self.progressbar = ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=100)

    def offline_help(self):
        print("offline_help")

    def online_help(self):
        print("online_help")

    def developer(self):
        print("developer")

    def project(self):
        print("project")

    def input_dir_change(self):
        self.incorrect_input_1.config(text="")
        self.text_input = filedialog.askopenfilename(filetypes = [("Text file", "*.txt")], title='Select a text file')
        self.file_input.set(self.text_input)

    def output_dir_change(self):
        self.incorrect_input_2.config(text="")
        self.text_output = filedialog.askdirectory()
        self.file_output.set(self.text_output)
        
    def check_checkbutton(self):
        self.checkbox_counter +=1
        if self.checkbox_counter % 2 == 1:
            self.check_sort_into = 1
            self.check_box_add = str(self.dir_output.get()) + "\\music"
            self.file_output.set(self.check_box_add)
            
        else:
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
       
            if self.input_find != "" and os.path.exists(self.input_find) == True:
                self.incorrect_input_1.grid_remove()
                with open(self.input_find, 'r+') as self.f:
                    self.lines = self.f.read().splitlines()
            
            elif self.input_type[0]!="":
                self.incorrect_input_1.grid_remove()
                counter = 0
                for element in self.input_type:
                    if len(element) < 45:
                        counter += 1
                        if counter == len(self.input_type):
                            self.lines = self.input_type
                    elif len(element) > 44:
                        self.incorrect_input_1.grid(row=5)
                        self.amount_labels +=1
                        self.incorrect_input_errors +=1
                        
                                
            else:
                self.incorrect_input_1.grid(row=5)
                self.amount_labels +=1
                self.incorrect_input_errors +=1

            self.output_loc = self.dir_output.get()
            if self.dir_output.get() != "" and os.path.exists(self.dir_output.get()):
                self.incorrect_input_2.grid_remove()
                self.output = self.dir_output.get()
            else:
                if self.amount_labels == 1:
                    self.incorrect_input_2.grid(row=6)
                    self.amount_labels +=1
                else:
                    self.incorrect_input_2.grid(row=5)
                    self.amount_labels +=1
                self.incorrect_input_errors +=1

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
                    

            if self.incorrect_input_errors == 0:
                thread_3 = threading.Thread(target=self.main_download, args=())
                thread_3.start()

            else:
                pass
        self.thread_2 = threading.Thread(target=download_start_main, args=())
        self.thread_2.start()
        
    def main_download(self):
        self.download_button.config(state="disabled")
        self.sort_into.config(state="disabled")
        self.dir_change_input.config(state="disabled")
        self.dir_change_output.config(state="disabled")
        self.progressbar.grid(row=5)
        self.progressbar.start(15)
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
            
            #converts to mp3
            if self.check_sort_into == 1:
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
            
            while True:
                if os.path.exists(initial_file):
                    time.sleep(2)
                    convert = Popen(convert_command)
                    break
                else:
                    pass

            time.sleep(10)
            while True:
                try:
                    os.remove(initial_file)
                    convert.terminate()
                    break
                except:
                    pass
                time.sleep(2)

        self.progressbar.stop()
        self.progressbar.grid_remove()
        self.completed.grid(row=5)

def first_run():
    os.system("pip install youtube-dl")
    #os.system("pip install pafy")
    print("Welcome")
    with open("runtime.txt", 'w') as r:
        r.write("1")
    run()
    
def run():
    root = tk.Tk()
    root.title("Main")
    root.geometry("648x380")
    root.resizable(width=False, height=False)
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    if os.path.exists("runtime.txt") == False:
        with open("runtime.txt", 'w') as write_runtime:
            write_runtime.write("0")

    with open("runtime.txt", 'r+') as r:
        read = r.readlines()
        if read[0] == "1":
            run()
        else:
            first_run()
