import file_utils


PREAMBLE = """ChatDev is a software company powered by multiple intelligent
 agents, such as chief executive officer, chief human resources officer, 
 chief product officer, chief technology officer, etc, with a multi-agent 
 organizational structure and the mission of "changing the digital world 
 through programming."""
GUI = "The software should be equipped with graphical user interface (GUI) so that user can visually and graphically use it; Ideally this should be done with no dependencies like canvas in html."

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mario Clone</title>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
    <div id="game-container">
        <canvas id="gameCanvas" width="800" height="400"></canvas>
    </div>
    <script src="script.js"></script>
</body>
</html>
"""

original_code = """
[index.html]

```html
{html_code}
```

[style.css]

css
/* CSS styles for the Mario clone */
body {
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #63a69f;
}

#game-container {
    text-align: center;
}

#gameCanvas {
    border: 2px solid #000;
}
[script.js]

javascript
Copy code
/*
Mario Clone Logic
*/

// Constants
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// Mario properties
const marioWidth = 32;
const marioHeight = 32;
let marioX = canvas.width / 2 - marioWidth / 2;
const marioY = canvas.height - marioHeight;
let marioSpeed = 5;
let isMovingLeft = false;
let isMovingRight = false;

// Event listeners for keyboard input
document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);

function keyDownHandler(event) {
    if (event.key === "Right" || event.key === "ArrowRight") {
        isMovingRight = true;
    }
    if (event.key === "Left" || event.key === "ArrowLeft") {
        isMovingLeft = true;
    }
}

function keyUpHandler(event) {
    if (event.key === "Right" || event.key === "ArrowRight") {
        isMovingRight = false;
    }
    if (event.key === "Left" || event.key === "ArrowLeft") {
        isMovingLeft = false;
    }
}

// Game update function
function update() {
    if (isMovingRight && marioX < canvas.width - marioWidth) {
        marioX += marioSpeed;
    }
    if (isMovingLeft && marioX > 0) {
        marioX -= marioSpeed;
    }
}

// Game render function
function render() {
    // Clear the canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw Mario
    ctx.fillStyle = "#ff0000"; // Red color for Mario
    ctx.fillRect(marioX, marioY, marioWidth, marioHeight);
}

// Game loop
function gameLoop() {
    update();
    render();
    requestAnimationFrame(gameLoop);
}

// Start the game loop
gameLoop();

```
"""
features = ["Player character (Mario) can move left and right using keyboard input.",
"Player character can jump using keyboard input",
"Player character can interact with the environment (e.g., platforms, obstacles).",
"Player character can collect items or power-ups",
"Collision detection to handle interactions with enemies or hazards",
"Scoring system to track and display the player's score",
"Level design and progression, including multiple levels with increasing difficulty",
"Implement enemies and obstacles with AI behavior",
"Implement game physics (e.g., gravity) for realistic character movement",
"Audio and sound effects for in-game actions",
"Implement a game menu with options to start, pause, and restart the game",
"Game over conditions and display of the final score",
"High score tracking and leaderboard functionality",
"Responsive design for various screen sizes and devices",
"Testing and debugging to ensure a bug-free gameplay experience",
"User interface improvements for a polished look and feel",
"Accessibility features to make the game playable for users with disabilities",
"Localization support for multiple languages",
"Performance optimization for smooth gameplay on various devices",
"Documentation and user instructions for how to play the game",
"Cross-browser compatibility to ensure the game works on different web browsers",
"Security measures to prevent cheating or tampering with the game",
"Regular updates and maintenance to address issues and improve the game over time",
]

def developer_initialize(task, role):
    return f""" 
According to the new user's task and our software designs listed below: 
Task: \"{task}\".
We have decided to complete the task through a executable software with
    a static html website. As the {role}, 
    to satisfy the new user's demands, you should write one or multiple 
    files and make sure that every detail of the architecture is, in the end, 
    implemented as code.
Think step by step and reason yourself to the right decisions to make sure we get it right.
You will output the content of the complete code. Each file must strictly follow a 
markdown code block format, where the following tokens must be replaced such that 
\"FILENAME\" is the lowercase file name including the file extension, \"LANGUAGE\" 
is the programming language and \"CODE\" is the original code.  The code should have
no comments, and you must respons with only the code and file-name... nothing

[FILENAME]
```LANGUAGE
CODE
```

For example:

[index.html]
```html
<!DOCTYPE html>
<html>
  <head>
  </head>
</html>
```

You will start with the \"[index.html]\" file, then go to the ones that are imported by that file, and so on.
Please note that the code should be fully functional. Ensure to implement all functions."""

def code_summarizer(file_name, code):
     return f"""
Your job is to give a high level description of the code for a given file.  
Think step by step and reason yourself to the right decisions to make sure we get it right.
The summary should be just a single sentence.  For example to summarize file_utils.js.

A javascript file used to read and write arbitrary data to files.

Code: \"{code}\"
     """

def code_reviewer(task, role, feature, code):
        return f""" 
According to the new user's task and our software designs listed below: 
Task: \"{task}\".
Feature: \"{feature}\"
We have decided to complete the task through a executable software with
a static html website. As a {role}, you are tasked with reviewing the code, and providing feedback.
Think step by step and reason yourself to the right decisions to make sure we get it right.
You will look at the code and provide feedback on it.

Remember, the best code is no code. Suggest only code changes, do not ask for comments
in the code, the code must be written without comments.  Also, do not suggest the developer
to run any programs, the only thing they can do is change the code.

Please provide comments as feedback to give to your fellow developer.
Your feedback must provide no formatting and be separated by new lines. The list must not have numbers or formatting.  Only write things to change.
You must only provide comments of things to change, do not provide any other commentary.
For example:

```
Feedback1
feedback2
feedback3
```

Below is the original code you are commenting on:

{code}

```

You will start with the \"[index.html]\" file, then go to the ones that are imported by that file, and so on.
Please note that the code should be fully functional. Ensure to implement all functions."""

def pm_feature_list(task, role):
    return f"""{PREAMBLE}
We have decided to complete the task through a executable software with
    a static html website. As the {role}, you are tasked with defining functional
    requirements for the {task}.  Each functional requirement must be able to be
    built independently of each other, and given to a programmer to implement.
    Think step by step and reason yourself to the right decisions to make sure we get it right.

    The functional requirements must be defined in a list separated by new lines.  The list must not have numbers or formatting
    For example:

    requirement1
    requirement2
    requirement3

"""

def developer_select_file_from_summary(task, summary):
    return f"""
        According to the new user's task and a summary of the software we have written below:
        Task: \"{task}\".
        Summary: \"{summary}\"

        Your job is to select which file to use to implement the new feature.
        Think step by step and reason yourself to the right decisions to make sure we get it right.
        If no file makes sense, please return none.

        Only respond with the file name or "none".  Do not respond with any other information.

        Example:

        main.py
    """     

# A follow up prompt to the developer to focus on implementing
# The given feature from a pm
def developer_feature_work(task, role, feature, original_code):
    return f""" 
According to the new user's task and our software designs listed below: 
Task: \"{task}\".
Feature: \"{feature}\"
We have decided to complete the task through a executable software with
a static html website. As the {role}, you have already implemented the code
below.  You have received a new feature requirement from your product manager.
Your task is to modify the code you have already written below to implement the feature.


Think step by step and reason yourself to the right decisions to make sure we get it right.
You will output the content of the complete code. Each file must strictly follow a 
markdown code block format, where the following tokens must be replaced such that 
\"FILENAME\" is the lowercase file name including the file extension, \"LANGUAGE\" 
is the programming languag and \"CODE\" is the original code:

[FILENAME]
```LANGUAGE
CODE
```

For example:

[index.html]
```html
<!DOCTYPE html>
<html>
  <head>
  </head>
</html>

Below is the original code you wrote:

{original_code}
```

You will start with the \"[index.html]\" file, then go to the ones that are imported by that file, and so on.
Please note that the code should be fully functional. Ensure to implement all functions."""

def developer_fix_code_review(task, role, feature, comments, original_code):
    return f""" 
According to the new user's task and our software designs listed below: 
Task: \"{task}\".
Feature: \"{feature}\"
We have decided to complete the task through a executable software with
a static html website. As the {role}, you have already implemented the code
below.  You have received feedback on the code from a fellow developer.

Your task is to modify the code you have already written below to respond to the comments
you have received.

Think step by step and reason yourself to the right decisions to make sure we get it right.
You will output the content of the complete code. Each file must strictly follow a 
markdown code block format, where the following tokens must be replaced such that 
\"FILENAME\" is the lowercase file name including the file extension, \"LANGUAGE\" 
is the programming languag and \"CODE\" is the original code:

[FILENAME]
```LANGUAGE
CODE
```

For example:

[index.html]
```html
<!DOCTYPE html>
<html>
  <head>
  </head>
</html>

Below are the comments followed by the original code:

{comments}

Original Code:

{original_code}
```

You will start with the \"[index.html]\" file, then go to the ones that are imported by that file, and so on.
Please note that the code should be fully functional. Ensure to implement all functions."""

def ux_describe_images(role, task, functional_requirements, html_code):
     return f"""
    We have decided to complete the task through a executable software with
    a static html website. As the {role}, you are tasked with defining images for "{task}"
    to go on the website.  Each image must have a title and a detailed description. Each image must be visually similar to the previous one.
    Think step by step and reason yourself to the right decisions to make sure we get it right.
    The description should be a Dalle-3 prompt.  Limit your response to the most impactful
    images to go on the website.
    Before you start, make sure the image will actually be displayed on the website.
    
    Below are the 
    functional requirements for the website:

    {functional_requirements}

    Here is the html code for the website:

    ```html
    {html_code}
    ```
    
    The output must be in the following format:

    [title]
    ```
    DESCRIPTION
    ```

    For example:

    [logo.png]
    ```
    Design a logo for a 2D platformer game inspired by Super Mario. The game is called 'Plumber Pete's Adventure'. It should feature a cartoonish plumber character with a red hat and overalls, jumping on a brick platform with a gold coin above him against a bright blue sky background.
    ```
   """

def full_stack_developer_place_images(role, task, image_data, html_code):
     return f"""
     After working with the UX Designer, they have designed images for the following task:
Task: \"{task}\".
We have decided to complete the task through a executable software with
a static html website. As the {role}, you have already implemented the code
below.  But, your job is to modify the code below to add the images the UX Designer
has designed (assuming they are relevant).  

Here are the urls and descriptions: {image_data}

Think step by step and reason yourself to the right decisions to make sure we get it right.
You will output the content of the complete code. Each file must strictly follow a 
markdown code block format, where the following tokens must be replaced such that 
\"FILENAME\" is the lowercase file name including the file extension, \"LANGUAGE\" 
is the programming languag and \"CODE\" is the original code:

[FILENAME]
```LANGUAGE
CODE
```

For example:

[index.html]
```html
<!DOCTYPE html>
<html>
  <head>
  </head>
</html>

Below is the original html code you wrote:

{html_code}
```
"""

# print(full_stack_developer_place_images("Full Stack Developer", "A burrito shop landing page", image_data, htm))
# print(ux_describe_images("UX Designer", "task", features, html_code))
# print(pm_features("A mario clone", "Product Manager"))
# print(developer_feature_work("A mario clone", "Developer", "Player character (Mario) can move left and right using keyboard input.", original_code))
# print(developer_first_prompt("A mario clone", "Developer"))
# print(code_reviewer("A mario clone", "Code Reviewer", features[1], original_code))
# print(code_summarizer('file_utils.py', file_utils.file_to_string('file_utils.py')))