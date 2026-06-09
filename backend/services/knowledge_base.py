from pathlib import Path


def load_knowledge_base() -> dict:
    project_root = Path(__file__).resolve().parents[2]
    knowledge_path = project_root / "data" / "knowledge_base"

    documents = {}

    if not knowledge_path.exists():
        return {
            "documents": {},
            "sources": [],
            "summary": "Knowledge base folder not found."
        }

    for file_path in knowledge_path.glob("*.md"):
        documents[file_path.name] = file_path.read_text(encoding="utf-8")

    return {
        "documents": documents,
        "sources": list(documents.keys()),
        "summary": f"{len(documents)} synthetic knowledge documents loaded."
    }