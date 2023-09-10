import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import face_recognition
import time


def select_input_directory():
    input_directory = filedialog.askdirectory()
    input_directory_entry.delete(0, tk.END)
    input_directory_entry.insert(tk.END, input_directory)

def select_output_directory():
    output_directory = filedialog.askdirectory()
    output_directory_entry.delete(0, tk.END)
    output_directory_entry.insert(tk.END, output_directory)

def select_known_faces_directory():
    known_faces_directory = filedialog.askdirectory()
    known_faces_directory_entry.delete(0, tk.END)
    known_faces_directory_entry.insert(tk.END, known_faces_directory)

def perform_face_filtering():
    input_directory = input_directory_entry.get()
    output_directory = output_directory_entry.get()
    known_faces_directory = known_faces_directory_entry.get()

    if not input_directory or not output_directory or not known_faces_directory:
        messagebox.showerror("Error", "Please select all directories.")
        return

    if not os.path.exists(input_directory):
        messagebox.showerror("Error", "Input directory does not exist.")
        return

    if not os.path.exists(known_faces_directory):
        messagebox.showerror("Error", "Known faces directory does not exist.")
        return

    #create output directory if doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Create a directory for images with no match
    no_match_directory = os.path.join(output_directory, "no_match")
    if not os.path.exists(no_match_directory):
        os.makedirs(no_match_directory)

    subfolders = [f for f in os.listdir(known_faces_directory) if os.path.isdir(os.path.join(known_faces_directory, f))]
    num_subfolders = len(subfolders)
    total_files = len(os.listdir(input_directory))
    processed_files = 0

    #create the progress bar
    percentage_label = tk.Label(window, text="0%", bg="#e5e5e5")
    percentage_label.place(x=200, y=300, anchor=tk.CENTER)

    progress_label = tk.Label(window, text="Progress: ", bg="#e5e5e5")
    progress_label.place(x=30, y=320, anchor=tk.W)

    progress_bar = tk.Canvas(window, width=200, height=20, bg="white", relief=tk.SUNKEN)
    progress_bar.place(x=200, y=320, anchor=tk.CENTER)

    # Iterate over the subdirectories in the known faces directory
    for person_name in os.listdir(known_faces_directory):
        person_directory = os.path.join(known_faces_directory, person_name)

        if not os.path.isdir(person_directory):
            continue  # Skip non-directory entries

        # Create a corresponding output directory for this person
        person_output_directory = os.path.join(output_directory, person_name)
        if not os.path.exists(person_output_directory):
            os.makedirs(person_output_directory)

        # Load the known face encodings for this person
        known_faces_encodings = []
        for file_name in os.listdir(person_directory):
            image = face_recognition.load_image_file(
                os.path.join(person_directory, file_name))
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                known_faces_encodings.extend(face_encodings)

        # Iterate over the input directory
        for file_name in os.listdir(input_directory):
            image_path = os.path.join(input_directory, file_name)

            # Load the input image
            image = face_recognition.load_image_file(image_path)

            # Find face locations and encodings in the image
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            # Flag to indicate if any match is found
            match_found = False

            # Iterate over the face encodings in the image
            for face_encoding in face_encodings:
                # Compare the face encoding with the known face encodings
                matches = face_recognition.compare_faces(
                    known_faces_encodings, face_encoding)

                if any(matches):
                    # Copy the image to the corresponding person's directory
                    shutil.copy2(image_path, person_output_directory)
                    print(
                        f"Image '{file_name}' contains a known face ({person_name}) and has been copied to ({person_output_directory}) directory.")
                    match_found = True
                    break

            if not match_found:
                # Move the image to the 'no_match' directory
                no_match_path = os.path.join(no_match_directory, file_name)
                shutil.copy2(image_path, no_match_path)
                print(
                    f"Image '{file_name}' does not contain a known face and has been moved to 'no_match' folder.")

            # Update the progress bar
            processed_files += 1
            progress_percentage = ((processed_files / total_files) * 100)/num_subfolders
            percentage_label["text"] = f"{int(progress_percentage)}%"
            progress_bar.create_rectangle(0, 0, progress_percentage * 2, 20, fill="#8bc34a")
            progress_bar.update()
            time.sleep(0.1)

    messagebox.showinfo("Success", "Face filtering complete.")


#main window
window = tk.Tk()
window.title("Face Filtering")
window.geometry("400x500")
window.resizable(False, False)
window.iconbitmap("icon.ico")
window.configure(bg="#e5e5e5")

"""
#background image
background_image = ImageTk.PhotoImage(Image.open("background.jpg"))
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
"""

#input 
input_directory_label = tk.Label(window, text="Select Input Directory:", bg="#e5e5e5")    #label
input_directory_label.place(x=70, y=30, anchor=tk.W)

input_directory_entry = tk.Entry(window, width=30)      #entry
input_directory_entry.place(x=70, y=60, anchor=tk.W)

input_directory_button = tk.Button(window, text="Browse...", command=select_input_directory, bg="#000000", fg="white", activebackground="#3b3b3b", activeforeground="white", relief=tk.FLAT, cursor="hand2")        #button
input_directory_button.place(x=260, y=60, anchor=tk.W)


#output
output_directory_label = tk.Label(window, text="Select Output Directory:", bg="#e5e5e5")    #label
output_directory_label.place(x=70, y=100, anchor=tk.W)

output_directory_entry = tk.Entry(window, width=30)          #entry
output_directory_entry.place(x=70, y=130, anchor=tk.W)

output_directory_button = tk.Button(window, text="Browse...", command=select_output_directory, bg="#000000", fg="white", activebackground="#3b3b3b", activeforeground="white", relief=tk.FLAT, cursor="hand2")         #button
output_directory_button.place(x=260, y=130, anchor=tk.W)


#known faces
known_faces_directory_label = tk.Label(window, text="Select Known Faces Directory:", bg="#e5e5e5")      #label
known_faces_directory_label.place(x=70, y=170, anchor=tk.W)

known_faces_directory_entry = tk.Entry(window, width=30)             #entry
known_faces_directory_entry.place(x=70, y=200, anchor=tk.W)

known_faces_directory_button = tk.Button(window, text="Browse...", command=select_known_faces_directory, bg="#000000", fg="white", activebackground="#3b3b3b", activeforeground="white", relief=tk.FLAT, cursor="hand2")           #button
known_faces_directory_button.place(x=260, y=200, anchor=tk.W)


#perform face filtering button
filter_button = tk.Button(window, text="Perform Face Filtering", command=perform_face_filtering, bg="#f44336", fg="black", activebackground="#d32f2f", activeforeground="white", relief=tk.FLAT, cursor="hand2")
filter_button.place(x=200, y=250, anchor=tk.CENTER)

#direction label
direction_label = tk.Label(window, text="* Input directory is the folder where there are photos to be filtered\n\n * Output directory is the folder to put the filtered photos\n\n * Known faces directory is the folder that has the known faces", bg="#e5e5e5")
direction_label.pack(side="bottom")

window.mainloop()
