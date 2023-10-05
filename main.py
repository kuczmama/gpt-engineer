import openai
import os
import subprocess
import re
import sys
import webbrowser
import threading
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer

openai.api_key = os.environ['OPENAI_API_KEY']

OUTPUT_DIRECTORY = "ai_generated_files"
CODE_SUBDIRECTORY = "code"
TEST_SUBDIRECTORY = "tests"
CODE_FILES = set()
MODEL = "gpt-3.5-turbo"
# MODEL = 'gpt-4'

CACHE_FILE = "response_cache.json"

# Ensure the output directory exists
if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

def load_cache():
    """Load cached data from the JSON file. If no file exists, return an empty dictionary."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_cache(cache_data):
    """Save data to the cache JSON file."""
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache_data, f, indent=4)



def run_web_server():
    os.chdir(OUTPUT_DIRECTORY)

    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(("localhost", 8000), handler)

    print("HTTP server started on port 8000.")
    httpd.serve_forever()

def get_response(messages):
    cache_data = load_cache()

    # Convert the list of messages to a string so it can be used as a key for the dictionary
    message_str = json.dumps(messages)

    # Check if the message exists in the cache
    if message_str in cache_data:
        print(f"\n[DEBUG - Cached Response]\n{cache_data[message_str]}\n[DEBUG END]\n")
        return cache_data[message_str]

    # If not in cache data, query OpenAI
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages
    )
    content = response.choices[0].message['content'].strip()
    print(f"\n[DEBUG - Assistant's Response]\n{content}\n[DEBUG END]\n")
    
    # Save the new response to the cache
    cache_data[message_str] = content
    save_cache(cache_data)
    
    return content

def sanitize_folder_name(name):
    """
    Transform the user's prompt into a valid folder name.
    """
    # Keep only alphanumeric characters and spaces
    sanitized_name = re.sub(r'[^a-zA-Z0-9 ]', '', name)
    # Replace spaces with underscores and lowercase everything
    sanitized_name = sanitized_name.replace(' ', '_').lower()
    # Limit the folder name's length to 50 characters
    return sanitized_name[:50]

def create_unique_folder(base_name):
    """
    Create a unique folder based on the base name.
    If the folder already exists, append a number to make it unique.
    """
    counter = 1
    folder_name = base_name
    while os.path.exists(os.path.join(OUTPUT_DIRECTORY, folder_name)):
        folder_name = f"{base_name}_{counter}"
        counter += 1
    os.makedirs(os.path.join(OUTPUT_DIRECTORY, folder_name))
    return folder_name

def write_to_file(folder_name, subdirectory, filename, content):
    """
    Save file to the specified subdirectory.
    """
    filepath = os.path.join(OUTPUT_DIRECTORY, folder_name, subdirectory, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"[File Created] {filepath}")
    if subdirectory == CODE_SUBDIRECTORY:  # Only add to the set if it's a code file and if it's not already in the set
        CODE_FILES.add(filepath)

def execute_test_script(test_file):
    try:
        feedback = subprocess.run(["python", os.path.join(OUTPUT_DIRECTORY, test_file)], capture_output=True, text=True)
        return feedback.stdout
    except subprocess.CalledProcessError as cpe:
        return f"Error during execution: {cpe.output}"
    except Exception as e:
        return f"Error: {e}"


def pm_breakdown_feature(user_input):
    pm_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Provide a list of functional requirements for a '{user_input}' into a detailed comma-separated list."}
    ]
    response = get_response(pm_messages)
    requirements = [req.strip() for req in response.split(",")]
    return requirements

def extract_code(content):
    # Return lines that look like code (e.g., don't contain commentary or markdown)
    return "\n".join([line for line in content.splitlines() if not line.startswith("```")])

def extract_multiple_files(content):
    # Find all occurrences of filename markers
    filenames = re.findall(r'\[filename\](.*?)\[/filename\]', content)
    
    # Split content based on the filename markers to extract file content
    file_contents = re.split(r'\[filename\].*?\[/filename\]', content)[1:]  # Ignoring the part before the first filename
    
    # Removing any extra whitespaces or newlines from both filenames and file contents
    filenames = [f.strip() for f in filenames]
    file_contents = [extract_code(c) for c in file_contents]
    
    return list(zip(filenames, file_contents))

def run_test_script(task, folder_name):
    """
    Create a test script for the task and run it.
    """
    test_files = qa_create_test(task, [])
    for filename, code in test_files:
        write_to_file(folder_name, TEST_SUBDIRECTORY, filename, code)
        print(f"\n[Testing File Created] {os.path.join(OUTPUT_DIRECTORY, TEST_SUBDIRECTORY, filename)}")

    # Move to the tests directory before executing tests
    os.chdir(os.path.join(OUTPUT_DIRECTORY, folder_name, TEST_SUBDIRECTORY))

    # Assuming the test files are Python scripts, execute them
    for filename, _ in test_files:
        feedback = execute_test_script(filename)
        print(feedback)

def extract_filename_and_code(response_content):
    # Regex pattern
    filename_pattern = r'\[(?P<filename>[a-zA-Z0-9_\-]+\.(?:html|css|js|py|java|cpp|go|rs|php|swift))\]'
    code_pattern = r'```(?:\w*\s*)?(.*?)```'

    filenames_and_codes = []

    while True:
        # Search for filename
        filename_match = re.search(filename_pattern, response_content)

        # If filename isn't found, break out of the loop
        if not filename_match:
            break

        # Get the position where the filename match ends
        filename_end_position = filename_match.end()

        # Search for the code block after the filename
        code_match = re.search(code_pattern, response_content[filename_end_position:], re.DOTALL)

        # If code isn't found after a filename, abort the program
        if not code_match:
            raise Exception("Code not found after filename in response. Aborting program.")

        # Get the filename from the matched group
        filename = filename_match.group('filename')

        # Extract the code content from the matched group
        code = code_match.group(1).strip()

        filenames_and_codes.append((filename, code))

        # Remove the matched filename and code from the content to continue the search
        response_content = response_content[:filename_match.start()] + response_content[filename_end_position + code_match.end():]

    # If no filename and code pairs are found, abort the program
    if not filenames_and_codes:
        raise Exception("No filename and code pairs found in response. Aborting program.")

    return filenames_and_codes



# TODO, prompt developer using files they have already written so they can re-use them
def developer_create_code(original_task, functional_requirement, previous_messages):
    dev_messages = previous_messages + [
        {"role": "user", "content": f"You are a software developer working on a '{original_task}', Please write the html/css/javascript/etc code for '{functional_requirement}'. Start your response with a filename suggestion enclosed in filename markers like [filename.js], followed by code in code markers like: ```python code_here```.  Ensure each code block has a file marker, and your response doesn't contain any other filename markers."}
    ]   
    response = get_response(dev_messages)
    return extract_filename_and_code(response)


def qa_create_test(task, previous_messages):
    # Format the information about the code files and their content by reading from the disk
    file_data_info = ""
    for filepath in CODE_FILES:
        with open(filepath, 'r') as f:
            content = f.read()
        file_data_info += f"File: {os.path.basename(filepath)}\nContent:\n{content}\n\n"

    qa_messages = previous_messages + [
        {"role": "user", "content": f"As a QA, provide a Selenium testing script (in Python).  Start your response with a filename suggestion enclosed in filename markers like [filename.py], followed by code in code markers like: ```python code_here```.  Ensure each code block has a file marker, and your response doesn't contain any other filename markers. You need to write the est for for '{task}'. Here are the code files and their content:\n\n{file_data_info}"}
    ]
    
    response = get_response(qa_messages)
    return extract_filename_and_code(response)

def main():
    while True:
        user_input = input("\nWhat web app feature do you want to create? ")
        # Create a unique folder for this session based on user input
        base_folder_name = sanitize_folder_name(user_input)
        current_folder_name = create_unique_folder(base_folder_name)

        # Create code and tests subdirectories for the current folder
        os.makedirs(os.path.join(OUTPUT_DIRECTORY, current_folder_name, CODE_SUBDIRECTORY))
        os.makedirs(os.path.join(OUTPUT_DIRECTORY, current_folder_name, TEST_SUBDIRECTORY))

        try:
            # Generate subtasks using the PM
            subtasks = pm_breakdown_feature(user_input)
            
            if not subtasks:
                print("Unable to generate subtasks. Try again.")
                continue
            
            # Define an initial context for the developer
            initial_dev_messages = [
                {"role": "system", "content": "You are a skilled software developer."},
                {"role": "user", "content": f"You are tasked with building a '{user_input}'. Please provide code for the feature."}
            ]
            
            for index, task in enumerate(subtasks):
                print(f"\n[Subtask {index + 1}] {task}")

                filenames_and_codes = developer_create_code(user_input, task, initial_dev_messages)
                for filename, code in filenames_and_codes:
                    write_to_file(current_folder_name, CODE_SUBDIRECTORY, filename, code)
                    print(f"\n[File Created] {os.path.join(OUTPUT_DIRECTORY, CODE_SUBDIRECTORY, filename)}")

                # Run tests
                test_choice = input("\nDo you want to run tests for this code? (yes/no): ").lower()
                if test_choice == 'yes':
                    web_server_thread = threading.Thread(target=run_web_server)
                    web_server_thread.start()
                    run_test_script(task, current_folder_name)

        except Exception as e:
            print(f"\n[ERROR] {str(e)}")
            sys.exit(1)  # Exit the program with an error code of 1

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
