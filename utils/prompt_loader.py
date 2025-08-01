from langchain_core.prompts import ChatPromptTemplate

def load_prompt_template(path: str) -> ChatPromptTemplate:
    with open(path, "r", encoding="utf-8") as f:
        template = f.read()
    return ChatPromptTemplate.from_template(template)
