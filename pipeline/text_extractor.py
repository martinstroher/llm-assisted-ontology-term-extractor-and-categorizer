import os
import pdftotext
import re

def extract(resources_path):
    def process_pdf(file_path):
        with open(file_path, "rb") as f:
            pdf = pdftotext.PDF(f)

        cleaned_texts = []
        for text in pdf:
            # Stop processing pages after acknowledgements OR references
            match = re.search(r"\backnowledgements\b|\bACKNOWLEDGEMENTS\b|\bACKNOWLEDGMENTS\b|\bAcknowledgements\b|\bREFERENCES\b|\bReferences\b", text)  # Combined regex
            if match:
                text = text[:match.start()]
                print(f"Stopped processing after {match.group()} (found on page {file_path})") # Which match
                break

            cleaned_text = "".join(char if char.isalnum() or char.isspace() else " " for char in text)
            cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()  # Normalize whitespace

            cleaned_texts.append(cleaned_text)

        return "\n\n".join(cleaned_texts)

    all_cleaned_texts = ""

    for filename in os.listdir(resources_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(resources_path, filename)
            print(f"Processing file: {filename}")

            cleaned_text = process_pdf(file_path)
            all_cleaned_texts += cleaned_text + "\n\n"

    output_file = "term_extraction/extracted_texts.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(all_cleaned_texts)

    print(f"Text extracted and saved to {output_file}")

    return all_cleaned_texts