import os

OUTPUT_DIRECTORY = "ai_generated_files"
CODE_SUBDIRECTORY = "code"
TEST_SUBDIRECTORY = "tests"
CODE_FILES = set()

def sanitize_folder_name(name):
    import re
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

def write_to_file(project_folder_name, subdirectory, filename, content):
    """
    Save file to the specified subdirectory.
    """
    filepath = os.path.join(OUTPUT_DIRECTORY, project_folder_name, subdirectory, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"[File Created] {os.path.abspath(filepath)}")
    if subdirectory == CODE_SUBDIRECTORY:  # Only add to the set if it's a code file and if it's not already in the set
        CODE_FILES.add(filepath)

def get_code_directory(project_folder_name):
    return os.path.join(OUTPUT_DIRECTORY, project_folder_name, CODE_SUBDIRECTORY)