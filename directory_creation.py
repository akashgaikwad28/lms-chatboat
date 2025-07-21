import os

# Define the chatbot folder structure
structure = {
    "chatbot": [
        ".env",
        {"config": ["settings.py"]},
        {"chains": ["course_recommender.py", "faq_chain.py"]},
        {"agents": ["lms_agent.py"]},
        {"tools": ["lms_api_tool.py"]},
        {"prompts": ["recommend_prompt.txt", "faq_prompt.txt"]},
        {"data": ["sample_courses.json"]},
        {"utils": ["helpers.py"]}
    ]
}

def create_structure(base_path, layout):
    for item in layout:
        if isinstance(item, str):
            file_path = os.path.join(base_path, item)
            with open(file_path, "w") as f:
                # Add a minimal placeholder
                if file_path.endswith(".py"):
                    f.write("# Placeholder for {}\n".format(item))
                elif file_path.endswith(".txt"):
                    f.write("# Prompt template: {}\n".format(item))
                elif file_path.endswith(".json"):
                    f.write("{\n  \"courses\": []\n}\n")
                elif file_path.endswith(".env"):
                    f.write("# Add your Gemini key and LMS API endpoint here\n")
        elif isinstance(item, dict):
            for folder, contents in item.items():
                subfolder_path = os.path.join(base_path, folder)
                os.makedirs(subfolder_path, exist_ok=True)
                create_structure(subfolder_path, contents)

def main():
    root_dir = "chatbot"
    os.makedirs(root_dir, exist_ok=True)
    create_structure(root_dir, structure[root_dir])
    print("✅ Chatbot structure created inside LMS project!")

if __name__ == "__main__":
    main()
