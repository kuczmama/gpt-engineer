import openai
import os
import re
import json
import prompts
import file_utils
from os import walk
import argparse
import webbrowser
import glob
from dalle3 import Dalle
import hashlib
import requests
from project_summary import ProjectSummary

CACHED_IMAGE_FOLDER = 'cached_images'

openai.api_key = os.environ['OPENAI_API_KEY']
DEFAULT_MODEL = "gpt-3.5-turbo-16k"

# INITIAL_DEVELOPER_MODEL = "ft:gpt-3.5-turbo-0613:personal::89edVQIv"
INITIAL_DEVELOPER_MODEL = "gpt-3.5-turbo-1106"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = "response_cache.json"
MAX_ITERATIONS = 1
IMAGE_SIZE = '256x256'
BING_COOKIE = os.getenv("BING_COOKIE") or ""
# Generate images based on the functional requirements and code
GENERIC_IMAGE_FOLDER = 'cached_images'


parser = argparse.ArgumentParser(description='argparse')
parser.add_argument('--task', type=str, default=None,
                    help="Prompt of software")
parser.add_argument('--name', type=str, default=None,
                    help="Name of software, your software will be generated in {fileutils.OUTPUT_DIRECTORY}")
parser.add_argument('--model', type=str, default=DEFAULT_MODEL,
                    help="GPT Model, choose from {'gpt-3.5-turbo-16k','gpt-4','gpt-3.5-turbo'}")
parser.add_argument('-dhi', '--disable-human-input', help="Enable human input", action='store_true')

args = parser.parse_args()
# print (f"Args: {args}")

MODEL = args.model
print("Using model: " + MODEL)
print("Task: ", args.task)
print("Name: ", args.name)
print("Disable Human input: ", args.disable_human_input)

# Ensure the output directory exists
if not os.path.exists(file_utils.OUTPUT_DIRECTORY):
    os.makedirs(file_utils.OUTPUT_DIRECTORY)

# Ensure generic image folder exists
if not os.path.exists(CACHED_IMAGE_FOLDER):
    os.makedirs(CACHED_IMAGE_FOLDER)

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


def get_response(messages, model=MODEL):
    print(f"""Get response from OpenAI. using model = {model}""")
    cache_data = load_cache()

    # Convert the list of messages to a string so it can be used as a key for the dictionary
    message_str = json.dumps(messages)
    print(f"\n[DEBUG - Assistant Input]\n#{message_str}\n[DEBUG END]\n")

    # Check if the message exists in the cache
    if message_str in cache_data:
        print(f"\n[DEBUG - Cached Response]\n{cache_data[message_str]}\n[DEBUG END]\n")
        return cache_data[message_str]

    # If not in cache data, query OpenAI
    response = openai.ChatCompletion.create(
        model=model,
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

def prompt(content, model=MODEL):
    messages = [
        {"role": "system", "content": prompts.PREAMBLE},
        {"role": "user", "content": content}
    ]
    return get_response(messages, model)

def pm_breakdown_feature(user_input):
    content = prompts.pm_feature_list(user_input, "Product Manager")
    response = prompt(content)
    requirements = [req.strip() for req in response.split("\n")]
    return requirements

def developer_initialize(user_input):
    content = prompts.developer_initialize(user_input, "Developer")
    response = prompt(content, INITIAL_DEVELOPER_MODEL)
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

def developer_summarize_file(file_name, code):
    content = prompts.code_summarizer(file_name, code)
    code_summary = prompt(content)
    return code_summary

def developer_select_file_from_summary(task, summary):
    content = prompts.developer_select_file_from_summary(task, summary)
    response = prompt(content)
    return response

def get_code_filepaths(current_folder_name):
    base_path = file_utils.get_code_directory(current_folder_name)
    files_paths = []
    for (dirpath, dirnames, filenames) in walk(base_path):
        for filename in filenames:
            file_path = os.path.join(base_path, filename)
            files_paths.append(file_path)
    return files_paths


def get_code_markdown_for_specific_file(file_path):
    filename = os.path.basename(file_path)
    file_path = os.path.join(file_path)
    language = filename.split('.')[-1]
    file_contents = open(file_path, 'r').read()
    response = ""
    response += f"[{filename}]\n"
    response += f"```{language}\n{file_contents}\n```"
    response += "\n\n"
    return response

def get_code_markdown_for_all_files(current_folder_name):
    file_paths = get_code_filepaths(current_folder_name)
    print("file_paths: ", file_paths)
    response = ""
    for file_path in file_paths:
        response += get_code_markdown_for_specific_file(file_path)

    return response
def persist_file_names_and_code(current_folder_name, filenames_and_codes):
    for filename, code in filenames_and_codes:
        file_utils.write_to_file(current_folder_name, file_utils.CODE_SUBDIRECTORY, filename, code)
    # Open a browser
    webbrowser.open(f"file://{os.path.realpath(file_utils.get_code_directory(current_folder_name))}/index.html",new=2)

# This function parses image prompts in the format
# [title]
# ```
# DESCRIPTION
# ```
# Return the image prompt like
# [{filename: 'filename', prompt: 'prompt'}]
#
# e.g. [{filename: 'image.jpg', prompt: 'A picture of a cat'}]
#
def parse_image_prompts(text):
    pattern = r'\[(.*?)\]\s+```\s(.*?)\s```'
    matches = re.findall(pattern, text, re.DOTALL)

    result = []
    for match in matches:
        data = {}
        data['filename'] = match[0]
        data['prompt'] = match[1].strip()
        filename, prompt = match
        print("File Name:", data['filename'])
        print("Prompt:", data['prompt'])
        print("----")
        result.append(data)
    return result

# Ensure generic image folder exists
if not os.path.exists(GENERIC_IMAGE_FOLDER):
    os.makedirs(GENERIC_IMAGE_FOLDER)

def generate_images(current_folder_name, user_input, functional_requirements, html_code):
    content = prompts.ux_describe_images(user_input, "UX Designer", functional_requirements, html_code)

    image_prompts = prompt(content)

    parsed_image_prompts = parse_image_prompts(image_prompts)
    image_details = []

    for image_prompt_data in parsed_image_prompts:
        filename = image_prompt_data['filename']
        img_prompt = image_prompt_data['prompt']
        breakpoint()

        # Create a hash of the prompt to be used for checking the cache
        prompt_hash = hashlib.sha256(img_prompt.encode()).hexdigest()

        local_image_path = os.path.join(GENERIC_IMAGE_FOLDER, filename)

        # Check if the image exists locally using the hash
        if prompt_hash in get_cached_prompts():
            image_details.append({
                'filename': filename,
                'prompt': img_prompt,
                'local_url': local_image_path
            })
            continue

        dalle = Dalle(BING_COOKIE)
        dalle.open_website(img_prompt)

        urls = dalle.get_urls()
        image_url = urls[0]  # Just using the first URL as in your example
        
        download_img_from_url(image_url, GENERIC_IMAGE_FOLDER, filename)

        # Update the cache
        add_to_cache(prompt_hash)

        image_details.append({
            'filename': filename,
            'prompt': img_prompt,
            'local_url': local_image_path
        })

    return image_details

def get_cached_prompts():
    # This function reads a simple cache file to get a set of hashed prompts
    with open('cache.txt', 'a+') as f:
        f.seek(0)  # Move to the beginning of the file before reading
        return set(line.strip() for line in f)

def add_to_cache(prompt_hash):
    # Appends a hashed prompt to the cache file
    with open('cache.txt', 'a') as f:
        f.write(prompt_hash + '\n')

def download_img_from_url(url, directory, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(os.path.join(directory, filename), 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

# Make sure you have the `requests` module installed: `pip install requests`

def get_html_code(current_folder_name):
    file_paths = get_code_filepaths(current_folder_name)
    result = []
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        file_path = os.path.join(file_path)
        language = filename.split('.')[-1]
        if language == 'html':
            file_contents = open(file_path, 'r').read()
            result.append(f"[{filename}]\n")
            result.append(f"```{language}\n{file_contents}\n```")
            result.append("\n\n")
    return result

# Get the code markdown for a specific file, or all files if none is specified
def get_code_markdown(current_folder_name, file_name):
    if file_name != "none":
        print(f"Developer selected file: {file_name}")
        file_path = os.path.join(file_utils.get_code_directory(current_folder_name), file_name)
        return get_code_markdown_for_specific_file(file_path)
    else:
        print("Get code markdown for all files")
        return get_code_markdown_for_all_files(current_folder_name)

# def place_images_in_html(current_folder_name, user_input, image_data, html_code):
#     content = prompts.full_stack_developer_place_images("Full Stack Developer",user_input, image_data, html_code)
#     breakpoint()
#     response = prompt(content)
#     breakpoint()
#     return extract_filename_and_code(response)

# TODO - use the summaries of the code to be able to program arbitrarily large code-bases
def main():
    user_input = args.task
    project_name = args.name
    # Fallback to asking the user what they want to do, if they don't se the command line arguments
    if (not user_input) or (not project_name):
        user_input = input("\nWhat web app feature do you want to create? ")
        project_name = user_input
    
    # Create a unique folder for this session based on user input
    project_folder_name = file_utils.sanitize_folder_name(project_name)
    current_folder_name = file_utils.create_unique_folder(project_folder_name)

    # # # Create code and tests subdirectories for the current folder
    os.makedirs(os.path.join(file_utils.OUTPUT_DIRECTORY, current_folder_name, file_utils.CODE_SUBDIRECTORY))

    project_summary = ProjectSummary()

    for i in range(MAX_ITERATIONS):
        print(f"\n[Iteration {i + 1}]")
        print("[Debug] Generating subtasks for PM")
        subtasks = pm_breakdown_feature(user_input)
        print(f"PM Generated ({len(subtasks)} subtasks)")
        if not subtasks:
            print("Unable to generate subtasks. Try again.")
            continue

        filenames_and_codes = developer_initialize(user_input)
        persist_file_names_and_code(current_folder_name, filenames_and_codes)
        # Summarize the project
        for filename, code in filenames_and_codes:
            summary = developer_summarize_file(filename, code)
            project_summary.add_file_summary(filename, summary)
        print("Project summary:")
        print(project_summary.get_summary())

        print("Current Code:")
        print(get_code_markdown_for_all_files(current_folder_name))
        
        for subtask in subtasks:
            print(f"Handling subtask: {subtask}")
            file_name = developer_select_file_from_summary(subtask, project_summary.get_summary())

            filenames_and_codes = developer_handle_subtask(
                user_input,
                subtask,
                get_code_markdown(current_folder_name, file_name))
            persist_file_names_and_code(current_folder_name, filenames_and_codes)
            # Summarize the project
            for filename, code in filenames_and_codes:
                summary = developer_summarize_file(filename, code)
                project_summary.add_file_summary(filename, summary)
            print("Doing code review")
            ai_comments = get_code_review(user_input, subtask, get_code_markdown(current_folder_name, file_name))

            print("Fixing code from AI comments")
            filenames_and_codes = developer_fix_code_review(
                user_input,
                subtask,
                ai_comments,
                get_code_markdown(current_folder_name, file_name))
            # Summarize the project
            for filename, code in filenames_and_codes:
                summary = developer_summarize_file(filename, code)
                project_summary.add_file_summary(filename, summary)
            persist_file_names_and_code(current_folder_name, filenames_and_codes)

            # Place images in the code
            # image_data = generate_images(
            #     current_folder_name,
            #     user_input,
            #     "\n".join(subtasks),
            #     get_html_code(current_folder_name))

            # filenames_and_codes = place_images_in_html(current_folder_name, user_input, image_data, get_html_code(current_folder_name))
            # persist_file_names_and_code(current_folder_name, filenames_and_codes)

            # TODO - Summarize the project
            if not args.disable_human_input:
                print(f"Code can be found at {os.path.abspath(file_utils.get_code_directory(current_folder_name))}")
                # Open webbrowser with the code running
                user_comments = input("\nWhat feedback do you want to give? ")
                filenames_and_codes = developer_fix_code_review(
                    user_input,
                    subtask,
                    user_comments,
                    get_code_markdown(current_folder_name, file_name))
                # Summarize the project
                for filename, code in filenames_and_codes:
                    summary = developer_summarize_file(filename, code)
                    project_summary.add_file_summary(filename, summary)
                persist_file_names_and_code(current_folder_name, filenames_and_codes)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
