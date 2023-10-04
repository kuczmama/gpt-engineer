import openai
import os
import subprocess
import re
import sys
import webbrowser
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

openai.api_key = os.environ['OPENAI_API_KEY']

OUTPUT_DIRECTORY = "ai_generated_files"
MODEL = "gpt-3.5-turbo"

# Ensure the output directory exists
if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

def run_web_server():
    os.chdir(OUTPUT_DIRECTORY)

    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(("localhost", 8000), handler)

    print("HTTP server started on port 8000.")
    httpd.serve_forever()

def get_response(messages):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages
    )
    # Log the assistant's response for debugging
    content = response.choices[0].message['content'].strip()
    print(f"\n[DEBUG - Assistant's Response]\n{content}\n[DEBUG END]\n")
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

def write_to_file(folder_name, filename, content):
    """
    Modified write_to_file function to include the folder_name.
    """
    filepath = os.path.join(OUTPUT_DIRECTORY, folder_name, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"[File Created] {os.path.join(OUTPUT_DIRECTORY, folder_name, filename)}")


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

def extract_filename_and_code(response_content):
    # Regex patterns
    filename_pattern = r'\[filename\](?P<filename1>.*?)\[/filename\]\s*|\[(?P<filename2>[a-zA-Z0-9_\-]+\.(?:html|css|js)?)\]\s*'
    code_pattern = r'```(?:\w*\s*)?(.*?)```'  # updated regex pattern for code block

    filenames_and_codes = []

    while True:
        # Search for filename
        filename_match = re.search(filename_pattern, response_content)

        # If filename isn't found, break out of the loop
        if not filename_match:
            break

        # Get the filename. Use the appropriate named group based on which pattern matched
        filename = filename_match.group('filename1') or filename_match.group('filename2')
        # Remove the matched filename from the content to continue the search later
        response_content = response_content.replace(filename_match.group(0), '', 1)

        # Search for the code block
        code_match = re.search(code_pattern, response_content, re.DOTALL)  # Added re.DOTALL for multi-line matching

        # If code isn't found after a filename, abort the program
        if not code_match:
            raise Exception("Code not found after filename in response. Aborting program.")

        # Remove the matched code from the content
        response_content = response_content.replace(code_match.group(0), '', 1)
        code = code_match.group(1).strip()

        filenames_and_codes.append((filename, code))

    # If no filename and code pairs are found, abort the program
    if not filenames_and_codes:
        raise Exception("No filename and code pairs found in response. Aborting program.")

    return filenames_and_codes



def developer_create_code(original_task, functional_requirement, previous_messages):
    dev_messages = previous_messages + [
        {"role": "user", "content": f"You are a software developer working on a '{original_task}', Please write the html/css/javascript/etc code for '{functional_requirement}'. Start your response with a filename suggestion enclosed in [filename]filename_here.ext[/filename], followed by the code."}
    ]
    response = get_response(dev_messages)
    return extract_filename_and_code(response)


def qa_create_test(task, previous_messages):
    qa_messages = previous_messages + [
        {"role": "user", "content": f"As a QA, provide a Selenium testing script (in Python) for '{task}'. Start your response with a filename suggestion enclosed in [filename]...[/filename] markers."}
    ]
    response = get_response(qa_messages)
    return extract_filename_and_code(response)

def main():
    while True:
        user_input = input("\nWhat web app feature do you want to create? ")
        # Create a unique folder for this session based on user input
        base_folder_name = sanitize_folder_name(user_input)
        current_folder_name = create_unique_folder(base_folder_name)

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
                    write_to_file(current_folder_name, filename, code)
                    print(f"\n[File Created] {os.path.join(OUTPUT_DIRECTORY, filename)}")

            run_choice = input("\nDo you want to run the web files? (yes/no): ").lower()
            if run_choice == 'yes':
                # Start the server in a separate thread
                web_server_thread = threading.Thread(target=run_web_server)
                web_server_thread.start()

                # A way to pause the main thread and let the user test the web app.
                # You can press Enter to stop the server and continue the main program.
                input("\nPress Enter when you're done testing the web app.")
                # Stopping the server (this method is a bit abrupt, ideally you would have a more graceful way)
                os._exit(0)
            
            # 3. Ask about any problems or bugs
            modify_choice = input("\nDid you encounter any problems or bugs? (yes/no): ").lower()

            # 4. Decide next steps
            if modify_choice == 'yes':
                # Loop back to the development phase
                continue
            else:
                print("\nThanks for using the program!")
                break

        except Exception as e:
            print(f"\n[ERROR] {str(e)}")
            sys.exit(1)  # Exit the program with an error code of 1

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
