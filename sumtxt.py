import os
import openai
import argparse
import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

openai.api_key = os.getenv('OAI_KEY')
OPENAI_MODEL="gpt-3.5-turbo"
MAX_TOKENS=1024

parser = argparse.ArgumentParser(description='Summarize a text document.')
parser.add_argument('filename', metavar='f', type=str, nargs=1,
                    help='the file to be summarized')

#nlp = spacy.load()
args = parser.parse_args()
# Set the string that will contain the summary

summary_text = ""
# Open the file
file_name = args.filename[0]
file_path = os.getcwd()
full_file_path = os.path.join(file_path, file_name)

# Read the text file line by line
paragraphs=[]
thisparagraph=""
last_line="" #including the previous line to bridge paragraphs
plength=0
flag=1
with open(full_file_path, 'r') as file:
    for line in file:
        linelength=num_tokens_from_string(line, OPENAI_MODEL)
        #print(f"length: {linelength}")
        #if adding this line to the paragraph doesn't exceed maxlength, do so
        if plength+linelength < MAX_TOKENS:
            thisline=line.strip()
            thisparagraph=thisparagraph + " " + thisline
            last_line=thisline
            plength=plength+linelength
            flag=1
        else:
            #we need to create a new paragraph
            paragraphs.append(thisparagraph)
            thisline=line.strip()
            thisparagraph=last_line + " " + thisline
            last_line=thisline
            plength=num_tokens_from_string(thisparagraph, OPENAI_MODEL)
            flag=0

#the last paragraph under construction was most likely not appended in the above loop
if flag:
    paragraphs.append(thisparagraph)


# Loop through all the paragraphs
for p in paragraphs:
    #print(p)
    
    response = openai.ChatCompletion.create(
                    model=OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a helpful research assistant and university educator."},
                        {"role": "user", "content": f"Concisely summarize this using language appropriate for a technical audience: {p}"},
                            ],
                                )
    page_summary = response["choices"][0]["message"]["content"]
    summary_text+=page_summary + "\n"
    summary_file = full_file_path.replace(os.path.splitext(full_file_path)[1], "_summary.txt")
    with open(summary_file, "w+") as file:
        file.write(summary_text)
    
