import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import docx
import PyPDF2
from style import *

roles = [
    "Quality Assurance", "Software Developer", "Data Analyst", "UI/UX Designer",
    "Project Manager", "Teacher", "Accountant", "Nurse", "Digital Marketer",
    "HR Manager", "Sales Executive", "Graphic Designer", "Chef", "Architect",
    "Writer", "Lawyer", "Business Analyst"
]

cv_sections = ["Summary", "Skills", "Experience", "Projects", "Education", "Certifications"]

role_keywords = {
    "Quality Assurance": ["test", "qa", "automation", "manual", "bug", "testing", "requirements", "quality", "methodology", "test case", "defect"],
    "Software Developer": ["java", "python", "developer", "programming", "database", "coding", "framework", "api", "frontend", "backend", "git", "html", "css", "javascript"],
    "Data Analyst": ["data analysis", "excel", "statistics", "data cleaning", "python", "R", "machine learning", "SQL", "data visualization", "graphs", "pivot tables"],
    "UI/UX Designer": ["design", "user interface", "user experience", "Figma", "Adobe XD", "prototyping", "wireframes", "visual design", "interaction design", "responsive design"],
    "Project Manager": ["project management", "agile", "scrum", "team leadership", "milestones", "stakeholder", "risk management", "project planning", "budget management", "schedule"],
    "Teacher": ["teaching", "education", "students", "curriculum", "classroom", "subject", "lecture", "teaching methodologies", "class management"],
    "Accountant": ["finance", "accounting", "ledger", "audit", "tax", "balance", "statements", "budget", "debit", "credit", "financial reporting", "accounts payable", "accounts receivable"],
    "Nurse": ["patient care", "nursing", "medical", "healthcare", "hospital", "emergency", "medications", "clinical", "patient monitoring", "health assessment"],
    "Digital Marketer": ["SEO", "social media", "PPC", "content marketing", "email marketing", "branding", "Google Ads", "Facebook Ads", "analytics", "marketing strategies"],
    "HR Manager": ["recruitment", "employee relations", "performance management", "training", "staff development", "HR policies", "payroll", "labor laws"],
    "Sales Executive": ["sales", "client relations", "CRM", "business development", "cold calling", "lead generation", "negotiation", "closing deals", "sales targets", "marketing strategies"],
    "Graphic Designer": ["design", "Adobe Photoshop", "Illustrator", "vector graphics", "branding", "logo design", "illustration", "typography", "creative"],
    "Chef": ["cooking", "culinary", "kitchen management", "food safety", "recipe creation", "menu planning", "food presentation", "quality control"],
    "Architect": ["architecture", "design", "CAD", "blueprints", "building codes", "construction", "urban planning", "space planning", "3D modeling"],
    "Writer": ["writing", "content creation", "blogging", "copywriting", "editing", "proofreading", "research", "creative writing", "storytelling"],
    "Lawyer": ["law", "legal", "litigation", "contract", "court", "lawsuit", "defense", "plaintiff", "legal research", "advocacy", "negotiation"],
    "Business Analyst": ["requirements gathering", "stakeholder", "data analysis", "business process", "gap analysis", "user stories", "JIRA", "workflow", "UML", "functional specification", "agile", "scrum", "presentation", "wireframes"],
}

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

def check_cv_sections(text):
    sections_found = {section: False for section in cv_sections}
    for section in cv_sections:
        if section.lower() in text.lower():
            sections_found[section] = True
    return sections_found

def calculate_score(text, role):
    if not text or role not in role_keywords:
        return 0, {}

    keywords = role_keywords[role]
    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    score = int((len(found_keywords) / len(keywords)) * 100)
    feedback = {kw: ("Found" if kw in found_keywords else "Missing") for kw in keywords}
    return score, feedback

def upload_file():
    if not selected_role.get() or selected_role.get() == "Select a job role":
        messagebox.showwarning("Select Job Role", "Please choose a job role before uploading your resume.")
        return

    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Word files", "*.docx")])
    if not file_path:
        return

    if not (file_path.endswith(".pdf") or file_path.endswith(".docx")):
        messagebox.showerror("Invalid File Type", "Please upload only PDF or DOCX files.")
        return

    text = extract_text_from_file(file_path)
    if text:
        role = selected_role.get()
        score, feedback = calculate_score(text, role)
        sections_found = check_cv_sections(text)

        result_text = f" Role: {role}\n Resume Score: {score}/100\n\n"
        result_text += "\n CV Sections Check:\n"
        for section, found in sections_found.items():
            result_text += f"{section}: {'Found' if found else 'Missing'}\n"

        score_label.config(text=result_text, fg=score_positive_color)
        file_name_label.config(text=f" Uploaded File: {os.path.basename(file_path)}")
    else:
        score_label.config(text="Could not read content from file.", fg=error_color)

# GUI Setup
window = tk.Tk()
window.title("Universal Resume Scanner & Score Predictor")
window.geometry("850x550")
window.resizable(True, True)
window.config(bg=bg_color)

bg_image_path = r"D:\Projects\Resume-Scanner-Score-Predictor\Resume_Score_Project\resume.png"
bg_image_label = None

def set_background_image(event=None):
    global bg_image_label
    if os.path.exists(bg_image_path):
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((event.width, event.height))
        bg_image_tk = ImageTk.PhotoImage(bg_image)

        if bg_image_label:
            bg_image_label.config(image=bg_image_tk)
            bg_image_label.image = bg_image_tk
        else:
            bg_image_label = tk.Label(window, image=bg_image_tk)
            bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_image_label.image = bg_image_tk
        bg_image_label.lower()

window.bind("<Configure>", set_background_image)
window.after(100, set_background_image)

frame = tk.Frame(window, bg=frame_bg_color, bd=frame_border, relief=frame_relief,
                 padx=frame_padding[0], pady=frame_padding[1])
frame.place(relx=0.5, rely=0.5, anchor="center")

title_label = tk.Label(frame, text="Resume Score Predictor", font=("Segoe UI", 26, "bold"),
                       fg=label_color, bg=frame_bg_color)
title_label.pack(pady=(10, 10))

# Role Dropdown & Instruction Message
selected_role = tk.StringVar()

# Update the instruction message
instruction_label = tk.Label(frame, text="Please choose a job role before uploading your resume.",
                             font=("Segoe UI", 12), fg="red", bg=frame_bg_color)
instruction_label.pack(pady=(5, 0))

def on_role_selected(*args):
    if selected_role.get() != "Select a job role":
        instruction_label.pack_forget()

selected_role.trace("w", on_role_selected)

# Add default option to dropdown
role_dropdown = tk.OptionMenu(frame, selected_role, "Select a job role", *roles)
role_dropdown.config(font=label_font, width=20, relief="raised", bg=highlight_color, fg="black", borderwidth=2)
role_dropdown.pack(pady=(10, 20))
selected_role.set("Select a job role")  # Set default option as "Select a job role"

upload_button = tk.Button(frame, text="Upload Here", command=upload_file, font=button_font,
                          bg=button_color, fg="white", relief="raised", bd=button_borderwidth,
                          width=button_width)
upload_button.pack(pady=10)

file_type_message = tk.Label(frame, text="(Only PDF and DOCX allowed)", font=("Segoe UI", 11),
                             fg="gray", bg=frame_bg_color)
file_type_message.pack(pady=(5, 15))

file_name_label = tk.Label(frame, text="No file uploaded yet", font=("Segoe UI", 12),
                           fg=label_color, bg=frame_bg_color)
file_name_label.pack(pady=(5, 10))

score_label = tk.Label(frame, text="", font=score_font, bg=frame_bg_color,
                       fg=score_color, justify="left", anchor="w")
score_label.pack(pady=20)

window.mainloop()
