# 🚀 DevTeam Simulation using ChatGPT

![Logo](res/logo2.jpeg)

## 🎯 Overview

Ever thought software development was just about typing away at keyboards? Think again! This project is where the magic of ChatGPT meets the intricacies of a software development team. Consisting of roles like:

- 🧠 Product Manager (PM) - The one who dreams it!
- 👩‍💻 Developer - The one who brings the dream to life!
- 🕵️‍♂️ Code Reviewer - The one who's looking for that misplaced semicolon!
- 🤔 Human Feedback - Because humans are... unpredictable.

Using OpenAI's ChatGPT, we don't just generate code; we craft masterpieces... iteratively, of course!

# Demo
🎥 Demo: Dive into the interactive experience and witness the magic of "GPT Engineer" in action. Prepare to be amazed! ✨

[![Watch the video](res/video-thumbnail.png)](https://youtu.be/gpQ95e6maEs)


## ✨ Features

- 💬 Uses OpenAI GPT models as our resident brainiac.
- 📋 Breakdown a grand idea into bite-sized tasks, all thanks to our virtual PM.
- 🧑‍🍳 Developer role: Code generation that feels like it's out of a Michelin star kitchen.
- 📝 Code Reviewer: More like a code whisperer, giving feedback on the code's deepest secrets.
- 👥 Accepts human emotions, err... I mean feedback.
- 🗃 A cache system so smart; it remembers what GPT said last summer!
- 📁 Generates code and neatly tucks them into their own cozy folders.

## 📚 Dependencies

- 🤖 OpenAI Python library.
- 🔧 Python's toolkit: os, re, json, argparse, webbrowser.

## How it works

This works by having a user, start with a prompt to the "Project Manager" agent.  The Project Manager, goes and creates tasks for the developer.  The developer then creates code, which is reviewed by the code reviewer.  On every iteration, this code is saved to a file which can be viewed in the browser.

![Arch](res/gpt-agents-arch.drawio.png)



## 🏗 Setup

1. 📂 Clone this magical repository.
2. 🗝 Got the OpenAI API key? No? Get it! Yes? Set it as `OPENAI_API_KEY` in your environment.
3. 🛠 Install the mystical packages:
pip install openai

## 🎮 How to Use

Fire up your terminal and say the magic spell:

```bash
python main.py --task "A snake game" --name "Retro Snake"
```

markdown
Copy code
Where:
- `--task`: Whisper your software desires here.
- `--name`: Name your masterpiece! It will live in the `ai_generated_files` directory.
- `--model`: (Optional) Name of your chosen OpenAI spirit. Default summons `gpt-3.5-turbo-16k`. You can also invoke `gpt-4` or `gpt-3.5-turbo`.
- `-dhi` or `--disable-human-input`: (Optional) Not in the mood for human interactions? Use this!

### 💡 Example
python <script_name>.py --task "Make a calculator to count the chickens before they hatch" --name "PreHatchCounter"

## 🎁 Output

Your wishes come true inside the `ai_generated_files` directory, housed in a folder bearing your software's name. If it's a web potion, drink in the magic from `index.html` using your trusty browser.

## 🧠 Cache System

Our genie remembers! Responses from OpenAI are preserved in `response_cache.json`, ensuring you don't repeat your wishes or break the bank.

## 📜 Open Source License

This treasure is open source. Seek it, modify it, spread the magic far and wide!

## 💬 Contribution

Magic is better with friends! Share spells, open issues, or submit potions through pull requests.

## ⚠️ Disclaimer

Before letting your creation loose in the wild, review the summoned code for any rogue genies or bugs. Remember, with great power comes... hilarious debugging sessions! 😉