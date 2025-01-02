import os
from transformers import GPT2Tokenizer
from openai import OpenAI

# Specify the directory path and blob path
path = r'C:\tools\ContextTest'
#the all-in-one string file, I use a ramdisk for speed, set to "" if do not want to store the blob
blob = r'R:\\'

# Set up the OpenAI client with a local server and API key
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Prompt the user to select a language
whatcode = input("What language is this code?\n 1. Python\n 2. C# MAUI\n 3. JavaScript\n 4. Java\n 5. Other\n")

if whatcode == "1":
    coding = "Python"
    extensions = [".py", ".env", ".json", ".xml", ".md", ".yml", ".yaml", ".ini", ".cfg", ".conf", ".txt"]
elif whatcode == "2":
    coding = "C# MAUI"
    extensions = [".cs", ".xaml", ".sln" , ".xml", ".json", ".config", ".csproj"]
elif whatcode == "3":
    coding = "JavaScript"
    extensions = [".js", ".html", ".css", ".json", ".xml"]
elif whatcode == "4":
    coding = "Java"
    extensions = [".java", ".xml", ".json", ".properties", ".gradle", ".md"]
elif whatcode == "5":
    coding = "Other only .txt files"
    extensions=[".txt"]

def get_files_recursively(path, extensions=extensions):
    # Get a list of files recursively in the specified directory
    files = []
    for root, dirs, filenames in os.walk(path):
        # Exclude unwanted directories
        dirs[:] = [d for d in dirs if d not in ['.vs', '.gt', 'bin', 'obj', 'backup', 'node_modules',  'dist', 'build',  'target']]
        filenames = [f for f in filenames if f.endswith(tuple(extensions))]
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

def read_utf8_file(file_path):
    # Read a file with UTF-8 encoding and return its contents
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            stringtext = file_path + "\n" + file.read()
            return stringtext
    except UnicodeDecodeError:
        # If the file is not a UTF-8 encoded text file, skip it
        return None

# Get a list of files recursively in the specified directory
files = get_files_recursively(path)

# Initialize counters and variables
files_nr = 0
file_contents = ""

for file in files:
    content = read_utf8_file(file)
    if content is not None:
        files_nr += 1
        print(f"Reading file {file}")
        # Append the file contents to the main string with a newline separator
        file_contents += "\n" + content

# Load the tokenizer (GPT2Tokenizer in this case)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

print(f"Number of files: {files_nr}")
print(f"Number of string characters: " + str(len(file_contents)))

# Tokenize the text and count the tokens
tokens = tokenizer.tokenize(file_contents)
number_of_tokens = len(tokens)

print("Number of tokens:", number_of_tokens)

if blob != "":
    # Write the combined contents to a new file (output.txt in this case)
    with open(blob + "output.txt", "w", encoding="utf-8") as output_file:
        output_file.write(file_contents)

# Check if the number of tokens is within the limits for various models
if number_of_tokens < 2048:
    print("You can use any Model (20,048):")
if number_of_tokens < 4096:
    print("You can use any LLama2 model (4,096):")
if number_of_tokens < 8192:
    print("You can use any LLama2 model (4,096):")
if number_of_tokens < 32768:
    print("You can use Mistral Models (32,768): ")
if number_of_tokens < 131072:
    print("You can use Command R or Phi 3 128k: (131,072): ")
if number_of_tokens < 1048576:
    print("You can use Llama 3 1048k: (1,048,576):")

first_question = input("Ask a question: about the files or code\n")

history = [
    {"role": "system", "content": f"You are a {coding} coding assistant. You are here to help with any {coding} Questions. Answer in short sentences and be clear. It is you duty to respond to the question with an answer."},
    {"role": "user", "content": file_contents + "\n" + first_question},
]

while True:
    completion = client.chat.completions.create(
        model="any",
        messages=history,
        temperature=0.7,
        stream=True
    )

    new_message = {"role": "assistant", "content": ""}

    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)

    # Uncomment to see chat history
    # import json
    # gray_color = "\033[90m"
    # reset_color = "\033[0m"
    # print(f"{gray_color}\n{'-'*20} History dump {'-'*20}\n")
    # print(json.dumps(history, indent=2))
    # print(f"\n{'-'*55}\n{reset_color}")

    print()
    history.append({"role": "user", "content": input("> ")})
