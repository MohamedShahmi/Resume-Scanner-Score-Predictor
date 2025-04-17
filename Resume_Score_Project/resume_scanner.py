import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import docx
import PyPDF2
from style import *  # Importing color and style settings from the style file

# Function to extract text from PDF or DOCX
def extract_text_from_file(file_path):
    try:
        if file_path.endswith(".pdf"):
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                return ''.join(page.extract_text() for page in reader.pages)
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            return '\n'.join(paragraph.text for paragraph in doc.paragraphs)
        else:
            return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Function to calculate a dummy score
def calculate_score(text):
    if not text:
        return 0
    keywords = ["python", "java", "team", "project", "experience", "development", "qa", "test"]
    score = sum(word.lower() in text.lower() for word in keywords)
    return min(score * 10, 100)

# Function triggered on Upload button
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")])
    
    if not file_path:
        return
    
    # Check if the file is PDF or DOCX
    if not (file_path.endswith(".pdf") or file_path.endswith(".docx")):
        messagebox.showerror("Invalid File Type", "Please upload only PDF or DOCX files.")
        return
    
    text = extract_text_from_file(file_path)
    if text:
        score = calculate_score(text)
        score_label.config(text=f"Resume Score: {score}/100", fg=score_positive_color)
    else:
        score_label.config(text="Could not read content from file.", fg=error_color)

# --- GUI Setup ---
window = tk.Tk()
window.title("Resume Scanner & Score Predictor")
window.geometry("800x500")
window.resizable(True, True)

# Load background image
bg_image_path = r"D:\Projects\Resume-Scanner-Score-Predictor\Resume_Score_Project\resume.png"
print(f"📂 Checking for image at: {bg_image_path}")

bg_image_label = None

def set_background_image(event=None):
    global bg_image_label
    if os.path.exists(bg_image_path):
        print("Image found, loading background...")
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((event.width, event.height))  # Resize based on window size
        bg_image_tk = ImageTk.PhotoImage(bg_image)

        if bg_image_label:
            bg_image_label.config(image=bg_image_tk)
            bg_image_label.image = bg_image_tk
        else:
            bg_image_label = tk.Label(window, image=bg_image_tk)
            bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_image_label.image = bg_image_tk
        bg_image_label.lower()  
    else:
        print("❌ Image not found! Please check the path and file name.")

# Bind resize event to update background
window.bind("<Configure>", set_background_image)

window.after(100, set_background_image)

# Main UI content
frame = tk.Frame(window, bg=frame_bg_color, bd=frame_border, relief=frame_relief, padx=frame_padding[0], pady=frame_padding[1])
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title label
title_label = tk.Label(frame, text="Upload Your Resume", font=("Helvetica", 28, "bold"), fg="black")  # No bg color
title_label.pack(pady=(20, 10))  # Close to the top, with some space

# Update button text to say "Upload Here"
upload_button = tk.Button(frame, text="Upload Here", command=upload_file, font=button_font, bg=button_color, fg="white", relief="raised", bd=5, width=20)
upload_button.pack(pady=10)

# Message to guide user about allowed file types
file_type_message = tk.Label(frame, text="(Only PDF and DOCX allowed)", font=("Helvetica", 12), fg="gray", bg=frame_bg_color)
file_type_message.pack(pady=(5, 20))

# Score label
score_label = tk.Label(frame, text="", font=score_font, bg=frame_bg_color, fg=score_color)
score_label.pack(pady=20)

window.mainloop()
