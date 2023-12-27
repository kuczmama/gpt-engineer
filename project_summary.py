# Summarize a project's high-level summary.  This summary is used to 
# be able to program arbitrarily large code-bases (similar to how a human would program).
# 
# If you think about it, humans don't work with the entire code-base at once, they will
# work with a small subset of the code-base at a time, and have a mental model of what the
# rest of the code-base does or use search.  This is an attempt to create a summary that
# can be passed into the context of the large-language model (LLM).

class ProjectSummary:
    def __init__(self):
        self.data = {}  # Dictionary to store file summaries

    def add_file_summary(self, file_name, summary):
        self.data[file_name] = summary

    def get_file_summary(self, file_name):
        return self.data.get(file_name, "")

    def get_summary(self):
        output = ""
        for file_name, summary in self.data.items():
            output += f"{file_name}: {summary}\n"
        return output