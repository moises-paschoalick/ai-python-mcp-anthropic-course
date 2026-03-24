import arxiv
import json
import os
from typing import List

PAPER_DIR = "papers"

def search_papers(topic: str, max_results: int = 5) -> List[str]:
    client = arxiv.Client()

    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = client.results(search)

    path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, "papers_info.json")

    try:
        with open(file_path, "r") as f:
            papers_info = json.load(f)
    except:
        papers_info = {}

    paper_ids = []

    for paper in papers:
        pid = paper.get_short_id()
        paper_ids.append(pid)

        papers_info[pid] = {
            "title": paper.title,
            "authors": [a.name for a in paper.authors],
            "summary": paper.summary,
            "pdf_url": paper.pdf_url,
            "published": str(paper.published.date())
        }

    with open(file_path, "w") as f:
        json.dump(papers_info, f, indent=2)

    return paper_ids

def extract_info(paper_id: str)  -> dict:
    if not os.path.exists(PAPER_DIR):
        return {"error": "No papers have been indexed yet"}

    for item in os.listdir(PAPER_DIR):
        item_path = os.path.join(PAPER_DIR, item)
        
        if not os.path.isdir(item_path):
            continue
        
        file_path = os.path.join(item_path, "papers_info.json")
        
        if not os.path.exists(file_path):
            continue
        
        try:
            with open(file_path, "r") as json_file:
                papers_info = json.load(json_file)
                
                if paper_id in papers_info:
                    return papers_info[paper_id]
        
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading {file_path}: {str(e)}")
            continue

    return {
        "error": f"No saved information found for paper {paper_id}"
    }