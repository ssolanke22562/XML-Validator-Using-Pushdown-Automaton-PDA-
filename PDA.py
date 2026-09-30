import tkinter as tk
from tkinter import filedialog
import re
import os

def validate_json_pda(data):
    stack = []
    pairs = {'}': '{', ']': '['}
    in_string = False
    escape = False
    
    for char in data:
        # Ignore brackets that are inside text strings
        if char == '"' and not escape:
            in_string = not in_string
        escape = (char == '\\' and not escape)
        
        if not in_string:
            if char in "{[":
                stack.append(char)          # PUSH
            elif char in "}]":
                if not stack or stack.pop() != pairs[char]: # POP
                    return False
                    
    return len(stack) == 0

def validate_xml_pda(data):
    stack = []
    # Regex to find XML tags and separate the closing slash, tag name, and self-closing slash
    # Example: <user id="1"> or </user> or <br/>
    tag_pattern = re.finditer(r'<(/)?([a-zA-Z0-9_-]+)[^>]*?(/)?>', data)
    
    for match in tag_pattern:
        is_closing = match.group(1)      # Contains '/' if it's </tag>
        tag_name = match.group(2)        # The actual name, e.g., 'user'
        is_self_closing = match.group(3) # Contains '/' if it's <tag/>
        
        if is_self_closing:
            continue                     # Skip self-closing tags (no stack action needed)
        elif not is_closing:
            stack.append(tag_name)       # PUSH opening tag
        else:
            if not stack or stack.pop() != tag_name: # POP closing tag
                return False
                
    return len(stack) == 0

def main():
    # Hide the background tkinter window
    root = tk.Tk()
    root.withdraw()
    
    # Open the file "upload" dialog
    print("Please select a JSON or XML file in the popup window...")
    file_path = filedialog.askopenfilename(
        title="Select File to Validate",
        filetypes=[("Data Files", "*.json *.xml")]
    )
    
    if not file_path:
        print("No file selected.")
        return

    # Read the uploaded file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # Route to the correct PDA parser
    if file_ext == '.json':
        is_valid = validate_json_pda(data)
    elif file_ext == '.xml':
        is_valid = validate_xml_pda(data)
    else:
        print("Unsupported file format.")
        return

    print(f"\nFile: {os.path.basename(file_path)}")
    print(f"Status: {'VALID ✓' if is_valid else 'INVALID ✗'}")

if __name__ == "__main__":
    main()