# MCP Anthropic ArXiv Chatbot

Educational project demonstrating how to build a tool-enabled chatbot using the Model Context Protocol (MCP) with Anthropic.

This project follows the course:

👉 https://learn.deeplearning.ai/courses/mcp-build-rich-context-ai-apps-with-anthropic

---

## 🚀 Overview

This chatbot allows users to:

- Search academic papers on arXiv
- Store results locally as JSON (papers ddirectory)
- Retrieve detailed information about specific papers
- Use Claude (LLM) to orchestrate tool execution

---

## 🧠 Architecture

```
User → Claude (LLM)
          ↓
      Tool Call (MCP)
          ↓
   Python Function (search_papers)
          ↓
   Tool Result → Claude → Final Answer
```

### Flow Example

```
User → Claude
        ↓
   search_papers()
        ↓
   JSON stored locally
        ↓
User asks about specific paper
        ↓
   extract_info()
        ↓
   Claude explains result

```

---

## 🛠️ Tools

### `search_papers`
- Searches arXiv
- Stores results in `papers/<topic>/papers_info.json`

### `extract_info`
- Retrieves paper details by ID
- Reads from local JSON storage

---

## 📁 Project Structure

```
├── main.py
├── tools.py
├── mcp_schema.py
├── papers/
├── .env
└── README.md

``` 

## ⚙️ Setup

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
### 2. Install dependencies
```
pip install -r requirements.txt

```

### 3. Configure environment
Create .env
```
ANTHROPIC_API_KEY=your_api_key_here
```

# Run
type exit to end the program.
```
python main.py
```