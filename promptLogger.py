import json
from datetime import datetime

class PromptLogger:
    def __init__(self, log_file="prompt_logs.jsonl"):
        self.log_file = log_file

    def log_prompt(self, data: dict):
        # Format the prompt
        context = "\n\n".join(data["chunks"])
        data["formatted_prompt"] = f"""
        You are an expert assistant for a custom t-shirt ecommerce platform.
        Use the following context to answer the user's query.
        If you don't know the answer, say so.

        Context:
        {context}

        Query: {data["user_query"]}
        Answer:
        """

        # Add timestamp
        data["timestamp"] = datetime.now().isoformat()

        # Write to JSONL file
        with open(self.log_file, "a") as f:
            f.write(json.dumps(data) + "\n")
