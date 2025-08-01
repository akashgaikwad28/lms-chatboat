# test_llm.py or temporary main.py

from utils.llm_provider import get_llm

llm = get_llm()
resp = llm.invoke("What is LangChain?")
print(resp.content)


