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

## Example:
```
--------------------------------------------------------------------------------------------------
Query: search for papers on algebra
--------------------------------------------------------------------------------------------------

Claude: Here is the search for papers on algebra:

 Calling tool search_papers with arg {'topic': 'algebra'}

Claude: The search returned 5 papers related to the topic of algebra. I've stored the paper IDs locally and you can now use the "extract_info" tool to get more details about any of these specific papers.


--------------------------------------------------------------------------------------------------
Query: yes please extract informaticon on the first two you found and summarize them both for me
--------------------------------------------------------------------------------------------------

Claude: Okay, let me first search for some papers on arXiv and then extract information on the top 2 results. 

 Calling tool search_papers with arg {'topic': 'machine learning'}

Claude: Now I will extract information on the top 2 results:

 Calling tool extract_info with arg {'paper_id': '2306.04338v1'}

 Calling tool extract_info with arg {'paper_id': '2006.16189v4'}

Claude: In summary:

Paper 1 (2306.04338v1) discusses the risks and challenges of changing data sources when using machine learning for official statistics. It provides a checklist of common issues and recommended precautions to maintain data integrity, reliability and relevance.

Paper 2 (2006.16189v4) proposes a set of community recommendations for better reporting and validation of supervised machine learning models in biological research. The goal is to help establish standards and better enable reviewers and readers to assess the performance and limitations of ML-based methods.

Both papers highlight important considerations around the use of machine learning, either in the context of official statistics or biological research. They provide practical guidance on ensuring the integrity and transparency of ML-based approaches.
```

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
or
python3.10 -m venv venv
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