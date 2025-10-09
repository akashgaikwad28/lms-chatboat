
# 🙌 LMS Chatbot with LangChain & Gemini

A modular chatbot for Learning Management Systems, powered by Google's Gemini via LangChain and served through FastAPI. Supports personalized course recommendations, concept explanations, and real-time LMS integration — all built with modern Python tooling (`uv`, `pyproject.toml`, async agents).

---

##  Features

-  **Multi-Intent Handling** – FAQ answering, counseling, concept explanation & more
-  **Gemini-Powered Responses** – Context-aware outputs via Google’s LLM
-  **Course Recommendation Engine** – Suggests relevant courses based on user input
-  **LMS API Integration** – Dynamically fetches courses and user info via tool layer
-  **Modular Agent Architecture** – Chains, tools, prompts, and agent routing separated
-  **Intent Classification via Prompts** – Routes queries to the correct sub-agent
-  **FastAPI Backend** – Exposes chat endpoint for UI or curl/Postman testing

---

## 🧩 Project Structure

```bash
.
├── main.py                  # FastAPI entry point
├── pyproject.toml           # uv + dependency management
├── .env                     # Contains API keys and config
│
├── agents/
│   └── lms_agent.py         # Main agent dispatcher
├── chains/
│   ├── course_recommender.py
│   ├── faq_chain.py
│   ├── concept_explainer.py
│   ├── counseling_chain.py
│   └── course_lookup.py
├── tools/
│   └── lms_api_tool.py      # Tool wrapper for LMS API calls
├── prompts/
│   ├── intent_classifier_prompt.txt
│   ├── recommend_prompt.txt
│   └── faq_prompt.txt
├── config/
│   └── settings.py          # Loads `.env` via pydantic-settings
├── utils/
│   └── llm_provider.py      # Central Gemini provider wrapper
├── data/
│   └── sample_courses.json  # Test data for RAG-like queries
└── test_llm.py              # Script to test LLM invocation
```

---

##  Getting Started

**1️⃣ Install uv globally (or use npx):**

```bash
npm install -g @manzt/uv
# OR
npx @manzt/uv pip install
```

**2️⃣ Install dependencies:**

```bash
npx @manzt/uv pip install
```

**3️⃣ Create a `.env` file with your API keys:**

```env
GEMINI_API_KEY=your_gemini_key
LMS_API_BASE_URL=https://your-lms.com/api
```

**4️⃣ Run the server:**

```bash
npx @manzt/uv run uvicorn main:app --reload
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📡 Sample Endpoints

| Route       | Method | Description                          |
|-------------|--------|--------------------------------------|
| `/`         | GET    | Health check                         |
| `/chat`     | POST   | Send a JSON query (`user_query`)     |

**Sample Request (curl):**

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"user_query\": \"Suggest a beginner course in DSA\"}"
```

---

##  How LangChain Is Used

- `faq_chain.py` – Responds to general questions via prompt + Gemini
- `course_recommender.py` – Uses sample data or API to recommend courses
- `lms_agent.py` – Classifies intent and dispatches sub-agents
- `llm_provider.py` – Unified Gemini LLM instantiation via `google_api_key`

---

## Developer Notes

- LangChain version: `>=0.3.26`
- Gemini via: `langchain-google-genai`
- Environment: `uv` + `.env` + `pyproject.toml`
- pydantic-settings: used for config loading
- Intent classifier prompt is chain-linked to Gemini via LangChain

---

##  Contributing

Pull requests welcome! Open issues for feature requests or discussion.

---

##  Greetings

Welcome to your LMS companion! 🙏  
Built to help students learn faster, ask smarter, and choose wisely 
