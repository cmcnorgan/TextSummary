import os
import PyPDF2
import re
import openai
import argparse

openai.api_key = os.getenv('OAI_KEY')
parser = argparse.ArgumentParser(description='Summarize a pdf document.')
parser.add_argument('filename', metavar='f', type=str, nargs=1,
                    help='the file to be summarized')

#nlp = spacy.load()
args = parser.parse_args()
# Set the string that will contain the summary

pdf_summary_text = ""
# Open the PDF file
file_name = args.filename[0]
pdf_path = os.getcwd()
pdf_file_path = os.path.join(pdf_path, file_name)
print(pdf_file_path)

# Read the PDF file using PyPDF2
pdf_file = open(file_name, 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file_path)
# Loop through all the pages in the PDF file
for page_num in range(len(pdf_reader.pages)):
    # Extract the text from the page
    page_text = pdf_reader.pages[page_num].extract_text().lower()
    page_text = page_text[:9192] + (page_text[9192:] and '..')
    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful research assistant and university educator."},
                        {"role": "user", "content": f"Concisely summarize this using language appropriate for a technical audience: {page_text}"},
                            ],
                                )
    page_summary = response["choices"][0]["message"]["content"]
    pdf_summary_text+=page_summary + "\n"
    pdf_summary_file = pdf_file_path.replace(os.path.splitext(pdf_file_path)[1], "_summary.txt")
    with open(pdf_summary_file, "w+") as file:
        file.write(pdf_summary_text)

pdf_file.close()

with open(pdf_summary_file, "r") as file:
    print(file.read())