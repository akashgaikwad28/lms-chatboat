
### 📘 `README.md`

```markdown
# 🧠 LMS Chatbot with LangChain & Gemini

A modular, Gemini-powered chatbot for LMS platforms built with FastAPI, LangChain, and modern Python tooling (`uv`). This bot answers FAQs, recommends personalized courses, and connects seamlessly to backend APIs and prompt templates.

---

## 🚀 Features

- 🔍 **FAQ Engine** – LangChain-powered responses to common student queries
- 🎓 **Course Recommender** – Personalized suggestions from course data
- 🔌 **LMS API Integration** – Connects with your live LMS backend
- 🧠 **Gemini-Powered Responses** – Rich context-aware answers via Google’s LLM
- 🛠️ **Modular Architecture** – Chains, agents, tools, and prompts split cleanly
- 📦 **Modern Environment** – No `venv` required thanks to `uv` + `pyproject.toml`
- ⚡ **FastAPI Backend** – Easily expose endpoints for bot communication

---

## 🗂️ Project Structure

```text
.
├── main.py                  # FastAPI entry point
├── pyproject.toml           # Dependency manager via `uv`
├── requirements.txt         # Optional legacy support
├── .env                     # Gemini key, LMS URL, etc.
│
├── config/
│   └── settings.py          # Loads config from `.env`
├── chains/
│   ├── course_recommender.py
│   └── faq_chain.py
├── agents/
│   └── lms_agent.py
├── tools/
│   └── lms_api_tool.py
├── prompts/
│   ├── recommend_prompt.txt
│   └── faq_prompt.txt
├── data/
│   └── sample_courses.json
└── utils/
    └── helpers.py
```

---

## ⚙️ Getting Started

### 1️⃣ Install `uv` if you haven’t

```bash
npm install -g @manzt/uv     # Or use: npx @manzt/uv
```

### 2️⃣ Install dependencies

```bash
npx @manzt/uv pip install
```

### 3️⃣ Create `.env` file

```env
GOOGLE_API_KEY=your-gemini-key-here
LMS_API_URL=https://your-lms.com/api
```

### 4️⃣ Start the FastAPI server

```bash
npx @manzt/uv run uvicorn main:app --reload
```

Visit: [http://localhost:8000](http://localhost:8000)

---

## 🧠 How LangChain Is Used

- `faq_chain.py` → Handles general question answering using Gemini + prompt
- `course_recommender.py` → RAG-style querying from sample course data
- `lms_agent.py` → Chooses tools based on query type
- `lms_api_tool.py` → Makes real LMS API calls as LangChain tools

---

## 📚 Sample Endpoints

| Route         | Method | Description                         |
|---------------|--------|-------------------------------------|
| `/`           | GET    | Basic health check                  |
| `/faq`        | POST   | Ask a general LMS question          |
| `/recommend`  | POST   | Get personalized course suggestions |

> (Add these in `main.py` to wire up your chains and agents)

---

## 👨‍💻 Developer Notes

- Built for backend extensibility and chatbot intelligence
- LangChain version `>=0.3.26`
- Gemini integration via `langchain-google-genai`
- Environment managed using `uv` and `pyproject.toml`

---

## 🤝 Contributing

Pull requests welcome! For major changes, please open an issue first to discuss what you'd like to improve or add.

---