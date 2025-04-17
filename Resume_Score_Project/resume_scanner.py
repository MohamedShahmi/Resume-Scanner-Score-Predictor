import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import docx
import PyPDF2
from style import * 

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
    if file_path:
        text = extract_text_from_file(file_path)
        if text:
            score = calculate_score(text)
            score_label.config(text=f"Resume Score: {score}/100", fg="green")
        else:
            score_label.config(text="Could not read content from file.", fg="red")

# --- GUI Setup ---
window = tk.Tk()
window.title("Resume Scanner & Score Predictor")
window.geometry("800x500")
window.resizable(True, True)

# Load background image
bg_image_path = r"D:\Projects\Resume-Scanner-Score-Predictor\Resume_Score_Project\resume.png"
print(f"📂 Checking for image at: {bg_image_path}")

bg_image_original = None
bg_image_label = None

def set_background_image(event=None):
    global bg_image_original, bg_image_label
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
frame = tk.Frame(window, bg="#ffffff", bd=2)
frame.place(relx=0.5, rely=0.5, anchor="center")

title_label = tk.Label(frame, text="Upload Your Resume", font=label_font, bg="#ffffff", fg="#2c3e50")
title_label.pack(pady=20)

upload_button = tk.Button(frame, text="Upload PDF or DOCX", command=upload_file, font=button_font, bg="#27ae60", fg="white")
upload_button.pack(pady=10)

score_label = tk.Label(frame, text="", font=score_font, bg="#ffffff", fg="black")
score_label.pack(pady=20)

window.mainloop()
