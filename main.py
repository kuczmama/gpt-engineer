import openai
import os
import re
import json
import prompts
import file_utils
from os import walk

openai.api_key = os.environ['OPENAI_API_KEY']
MODEL = "gpt-3.5-turbo-16k"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = "response_cache.json"
MAX_ITERATIONS = 1

# Ensure the output directory exists
if not os.path.exists(file_utils.OUTPUT_DIRECTORY):
    os.makedirs(file_utils.OUTPUT_DIRECTORY)

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

def extract_filename_and_code(response_content):
    print(f"Extract_filename_and_code")
    # Regex pattern
    filename_pattern = r'\[(?P<filename>[a-zA-Z0-9_\-]+\.(?:html|css|js|py|java|cpp|go|rs|php|swift))\]'
    code_pattern = r'```(?:\w*\s*)?(.*?)```'

    filenames_and_codes = []

    while True:
        # Search for filename
        filename_match = re.search(filename_pattern, response_content)

        # If filename isn't found, break out of the loop
        if not filename_match:
            print(f"No filename found in response. {response_content}")
            break

        # Get the position where the filename match ends
        filename_end_position = filename_match.end()

        # Search for the code block after the filename
        code_match = re.search(code_pattern, response_content[filename_end_position:], re.DOTALL)

        # If code isn't found after a filename, abort the program
        if not code_match:
            if len(filenames_and_codes) > 0:
                print(f"Code not found after filename in response. Returning {len(filenames_and_codes)} filenames and codes.")
                return filenames_and_codes
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

def prompt(content):
    messages = [
        {"role": "system", "content": prompts.PREAMBLE},
        {"role": "user", "content": content}
    ]
    return get_response(messages)

def pm_breakdown_feature(user_input):
    content = prompts.pm_feature_list(user_input, "Product Manager")
    response = prompt(content)
    requirements = [req.strip() for req in response.split("\n")]
    return requirements

def developer_initialize(user_input):
    content = prompts.developer_initialize(user_input, "Developer")
    response = prompt(content)
    return extract_filename_and_code(response)

def developer_handle_subtask(user_input, subtask, original_code):
    content = prompts.developer_feature_work(user_input, "Developer", subtask, original_code)
    response = prompt(content)
    return extract_filename_and_code(response)

def get_code_review(user_input, subtask, original_code):
    content = prompts.code_reviewer(user_input, "Code Reviewer", subtask, original_code)
    response = prompt(content)
    return response

def developer_fix_code_review(user_input, feature, comments, original_code):
    content = prompts.developer_fix_code_review(user_input, "Developer", feature, comments, original_code)
    response = prompt(content)
    return extract_filename_and_code(response)

def get_current_code_str(current_folder_name):
    base_path = file_utils.get_code_directory(current_folder_name)
    print(f"get_current_code: {base_path}")
    response = ""
    f = []
    for (dirpath, dirnames, filenames) in walk(base_path):
        f.extend(filenames)

    print("filenames: ", f)
    for filename in f:
        file_path = os.path.join(base_path, filename)
        print("path: ", file_path)
        open(file_path, 'r').read()
        response += f"[{filename}]\n"
        response += f"```{filename.split('.')[-1]}\n{open(file_path, 'r').read()}\n```"
        response += "\n\n"

    return response

def write_filenames_and_code(current_folder_name, filenames_and_codes):
    for filename, code in filenames_and_codes:
        file_utils.write_to_file(current_folder_name, file_utils.CODE_SUBDIRECTORY, filename, code)
        print(f"\n[File Created] {os.path.join(file_utils.OUTPUT_DIRECTORY, file_utils.CODE_SUBDIRECTORY, filename)}")

def main():
    user_input = input("\nWhat web app feature do you want to create? ")
    # Create a unique folder for this session based on user input
    project_folder_name = file_utils.sanitize_folder_name(user_input)
    current_folder_name = file_utils.create_unique_folder(project_folder_name)

    # # # Create code and tests subdirectories for the current folder
    os.makedirs(os.path.join(file_utils.OUTPUT_DIRECTORY, current_folder_name, file_utils.CODE_SUBDIRECTORY))
    
    for i in range(MAX_ITERATIONS):
        print(f"\n[Iteration {i + 1}]")
        print("[Debug] Generating subtasks for PM")
        subtasks = pm_breakdown_feature(user_input)
        print(f"PM Generated ({len(subtasks)} subtasks)")
        if not subtasks:
            print("Unable to generate subtasks. Try again.")
            continue

        filenames_and_codes = developer_initialize(user_input)
        write_filenames_and_code(current_folder_name, filenames_and_codes)

        print("Current Code:")
        print(get_current_code_str(current_folder_name))
        
        for subtask in subtasks:
            print(f"Handling subtask: {subtask}")
            # Update the current code based on the subtask
            filenames_and_codes = developer_handle_subtask(
                user_input,
                subtask,
                get_current_code_str(current_folder_name))
            write_filenames_and_code(current_folder_name, filenames_and_codes)
            print("Doing code review")
            comments = get_code_review(user_input, subtask, get_current_code_str(current_folder_name))
            print("Fixing code")
            filenames_and_codes = developer_fix_code_review(
                user_input,
                subtask,
                comments,
                get_current_code_str(current_folder_name))
            write_filenames_and_code(current_folder_name, filenames_and_codes)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
