import tkinter as Tk     # from tkinter import Tk for Python 3.x
from tkinter import ttk, filedialog
import os
import zipfile


ESCRIPTION = """
This program unzips multiple times (to diferent task folders) a zip file 
    of your cpp code and builds it with cmake to each build folder.

    e.x. 
        input: file path: C:\ ... \ lab02.zip
        input: folder path: C:\ ... \\targetfolder
        input: task number: 2

        output:
            created folder 1: C:\ ... \\targetfolder\\TASK_1 
                contains the unziped file lab02
                and inside the lab02 is created a build folder with
                the compiled project lab02.

            created folder 2: C:\ ... \\targetfolder\\TASK_2 
                contains the unziped file lab02
                and inside the lab02 is created a build folder with
                the compiled project lab02.


The task number defines the number of copies that will be created, 
    also each copy is placed in a different folder, named: "TASK_i".

The select file button pops out a window, and the user selects the bace
    .zip file which it will be upziped.

In the folder section the user selects a target path, which is going to 
    contain the subfolders "TASK_1","TASK_2", ... .
"""

ZIP_PATH = ""
TARGET_FOLDER_PATH = ""
TASKS = 1
show_info_is_true = True    


def select_file():
    global ZIP_PATH, select_file_label
    ZIP_PATH = filedialog.askopenfile(filetypes=[("all file format", ".zip")])
    if ZIP_PATH != None:
        ZIP_PATH = ZIP_PATH.name
        if zipfile.is_zipfile(ZIP_PATH) :
            try: select_file_label.destroy()
            except: pass
            select_file_label = Tk.Label(buttons_frame, text = f"target file: {ZIP_PATH}")
            select_file_label.grid(row = 2, column = 0, columnspan = 2)    

def select_folder():
    global TARGET_FOLDER_PATH, select_folder_label
    TARGET_FOLDER_PATH = filedialog.askdirectory()
    if os.path.isdir(TARGET_FOLDER_PATH):
        try: select_folder_label.destroy()
        except: pass
        select_folder_label = Tk.Label(buttons_frame, text = f"target folder: {TARGET_FOLDER_PATH}")
        select_folder_label.grid(row = 4, column = 0, columnspan = 2)

def extract():
    if not zipfile.is_zipfile(ZIP_PATH) or not os.path.isdir(TARGET_FOLDER_PATH): 
        print("Files path error")
        return False
    
    TASKS = input_tasks_number.get()
    if not TASKS.isnumeric(): 
        print("Invalid input as a Task number")
        return False
    
    TASKS=int(TASKS)
    if not os.path.exists(TARGET_FOLDER_PATH):
        os.makedirs(TARGET_FOLDER_PATH)

    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        for i in range(TASKS):
            # unzip 
            target_path = TARGET_FOLDER_PATH + "/TASK_"+str(i+1)
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            zip_ref.extractall(target_path)
            
            # call cmake here
            # μονο αμα υπαρχει το αρχειο CMakeLists.txt εκτελω cmake

            filename = ZIP_PATH.split("/")[-1].split(".")[0]
            extracted_path = target_path + "/"+filename
            build_path = extracted_path + "/"+ "build"
            
            do_cmake = False
            listOfFileNames = os.listdir(extracted_path)  
            for file in listOfFileNames:
                if file=='CMakeLists.txt':
                    do_cmake = True
                    break
            if not do_cmake: continue

            if not os.path.isdir(build_path):
                os.makedirs(build_path)

            os.system(f"cmake -S {extracted_path} -B {build_path}")

def show_info():
    global read_me_text, show_info_is_true
    if show_info_is_true:
        read_me_text = Tk.Text(root, width = 77, height = 20)
        read_me_text.insert("end", ESCRIPTION)
        read_me_text.grid(row = 0, column = 1)
    else:
        read_me_text.destroy()
    show_info_is_true = not show_info_is_true
    

root = Tk.Tk()
root.title("Extracter 🎁")
buttons_frame = Tk.Frame(root)
buttons_frame.grid(row = 0, column = 0)
tasks_number_label = Tk.Label(buttons_frame, text = "number of tasks:", font = "Arial 12 bold", )
input_tasks_number = Tk.Entry(buttons_frame, width = 5, font = "Arial 12 bold")
select_file_button = Tk.Button(buttons_frame, text = "select file", fg = "blue", font = "Arial 14 bold", command = select_file)
select_folder_button = Tk.Button(buttons_frame, text = "select folder", fg = "red", font = "Arial 14 bold", command = select_folder)
separator = ttk.Separator(buttons_frame, orient = "horizontal")
extract_button = Tk.Button(buttons_frame, text = "extract", bg = "green", fg = "white", font = "Arial 20 bold", width = 12, command = extract)
how_to_use_button = Tk.Button(buttons_frame, text = "how to use", bg = "white", font = "Arial 10 bold", command = show_info)

tasks_number_label.grid(row = 0, column = 0, padx = 5, pady = 15, sticky = Tk.E)
input_tasks_number.grid(row = 0, column = 1, padx = 5, pady = 15, sticky = Tk.W)
select_file_button.grid(row = 1, column = 0, columnspan = 2, pady = 5)
select_folder_button.grid(row = 3, column = 0, columnspan = 2, pady = 5)
separator.grid(row = 5, column = 0, columnspan = 2, pady = 10)
extract_button.grid(row = 6, column = 0, columnspan = 2, padx = 20, pady = 10)
how_to_use_button.grid(row = 7, column = 0, columnspan = 2, pady = 10)

root.mainloop()

print(f"Extracting {ZIP_PATH} to target folder {TARGET_FOLDER_PATH}")