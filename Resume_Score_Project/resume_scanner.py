import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pdfplumber
import docx
from style import button_style, label_style, title_style, result_style, bg_color

# Extract text from file
def extract_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        try:
            with pdfplumber.open(filepath) as pdf:
                return '\n'.join(page.extract_text() for page in pdf.pages if page.extract_text())
        except Exception as e:
            return f"Error reading PDF: {e}"

    elif ext == ".docx":
        try:
            doc = docx.Document(filepath)
            return '\n'.join([p.text for p in doc.paragraphs])
        except Exception as e:
            return f"Error reading DOCX: {e}"
    
    return "Unsupported file type."

# Score based on keywords
def score_resume(text):
    keywords = [
        "python", "java", "sql", "api", "automation", "testing",
        "jira", "selenium", "rest", "quality", "postman",
        "unit test", "test case", "bug", "agile"
    ]
    score = sum(1 for kw in keywords if kw in text.lower())
    total_score = int((score / len(keywords)) * 100)
    return total_score

# Generate improvement tips
def generate_tips(score):
    if score >= 90:
        return "Excellent resume! You're showcasing all key skills."
    elif score >= 60:
        return "Good job! Try to highlight a few more QA or tech skills."
    else:
        return "Improve your resume with more relevant skills and tools."

# Upload and analyze file
def upload_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")],
        title="Select Resume File"
    )
    
    if file_path:
        result_label.config(text="Analyzing resume...")
        root.update()
        
        text = extract_text(file_path)
        if "Error" in text or "Unsupported" in text:
            result_label.config(text="❌ " + text)
        else:
            score = score_resume(text)
            tip = generate_tips(score)
            result_label.config(text=f"✅ Resume Score: {score}/100\n\n💡 {tip}")

#GUI setup
root = tk.Tk()
root.title("Smart Resume Scanner")
root.geometry("500x350")
root.configure(bg=bg_color)  # Set background color

# Enable maximize option
root.resizable(True, True)

# Title Label
title_label = tk.Label(root, text="Upload your resume (.pdf or .docx)", **title_style)
title_label.pack()

# Upload Button
upload_btn = tk.Button(root, text="Upload Resume", command=upload_file, **button_style)
upload_btn.pack()

# Result Label
result_label = tk.Label(root, text="", **result_style)
result_label.pack()

root.mainloop()
