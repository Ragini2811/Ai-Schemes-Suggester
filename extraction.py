import os
import cv2
import pytesseract
import spacy
import re
import csv
import editdistance
from fuzzywuzzy import process

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Set Tesseract path (update this to your installation path)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Preprocess images
def preprocess_image(img_path):
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    return 255 - binary

# Extract text using Tesseract OCR
def extract_text_from_image(img):
    return pytesseract.image_to_string(img, lang='eng')

# Aadhaar extraction
def extract_aadhaar_details(front_img_path, back_img_path):
    front_img = preprocess_image(front_img_path)
    front_text = extract_text_from_image(front_img)
    back_img = preprocess_image(back_img_path)
    back_text = extract_text_from_image(back_img)
    name = extract_name(front_text)
    dob = extract_dob(front_text)
    State = extract_State_with_fuzzy(back_text)

    return {
        "Name": name,
        "Date of Birth": dob,
        "State": State
    }
    
from fuzzywuzzy import process

# Community Certificate extraction
def extract_community_details(img_path):
    img = preprocess_image(img_path)  # Your existing image preprocessing function
    text = extract_text_from_image(img)  # Your existing OCR extraction function
    
    community_name = extract_community_name(text)
    return {
        "Community Name": community_name if community_name else "Community Name Not Found"
    }

def extract_community_name(text):
    # List of community names
    community_names = ["BC", "ST", "SC", "OBC"]
    
    # Check for the presence of community names in the extracted text
    for community in community_names:
        if community.lower() in text.lower():
            return community  # Return the first matched community name
    
    return None

# Income Certificate extraction
def extract_income_details(img_path):
    img = preprocess_image(img_path)
    text = extract_text_from_image(img)
    income_match = re.search(r"Rs\. (\d+)\/annum", text)
    income_amount = income_match.group(1) if income_match else None
    return {"Income amount": income_amount}

# Utility functions for text extraction
def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_dob(text):
    date_pattern = r'\b\d{2}[-/]\d{2}[-/]\d{4}\b'
    dates = re.findall(date_pattern, text)
    return dates[0] if dates else None

def extract_state_number(text):
    match = re.search(r'\b\d{4} \d{4} \d{4}\b', text)
    return match.group(0) if match else None

def extract_State_with_fuzzy(text):
    states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", 
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", 
        "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", 
        "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", 
        "Uttar Pradesh", "Uttarakhand", "West Bengal"
    ]

    # Extract potential state names using fuzzy matching
    best_match = process.extractOne(text, states)
    if best_match:
        return f" {best_match[0]}"
    else:
        return "No state found in the text"
    