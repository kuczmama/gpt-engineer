import openai
import os
import subprocess
import re
import sys

openai.api_key = os.environ['OPENAI_API_KEY']

OUTPUT_DIRECTORY = "ai_generated_files"
MODEL = "gpt-4"

# Ensure the output directory exists
if not os.path.exists(OUTPUT_DIRECTORY):
    os.makedirs(OUTPUT_DIRECTORY)

def get_response(messages):
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages
    )
    # Log the assistant's response for debugging
    content = response.choices[0].message['content'].strip()
    print(f"\n[DEBUG - Assistant's Response]\n{content}\n[DEBUG END]\n")
    return content

def write_to_file(filename, content):
    filepath = os.path.join(OUTPUT_DIRECTORY, filename)
    with open(filepath, 'w') as f:
        f.write(content)

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
    pattern = r'\[filename\](.*?)\[\/filename\]\s*```\w+\s*(.*?)```'

    matches = re.findall(pattern, response_content, re.DOTALL)

    filenames_and_codes = []
    for match in matches:
        filename = match[0].strip()
        code = match[1].strip('`').strip()
        filenames_and_codes.append((filename, code))
    
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
                    write_to_file(filename, code)
                    print(f"\n[File Created] {os.path.join(OUTPUT_DIRECTORY, filename)}")


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
