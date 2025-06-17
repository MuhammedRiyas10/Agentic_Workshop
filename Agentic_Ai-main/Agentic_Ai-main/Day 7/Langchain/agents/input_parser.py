import os
from graph.schema import AgentState

def parse_input(state: AgentState) -> AgentState:
    """
    Parses the input file (text or PDF) into plain text.
    """
    source_path = state.input_path
    source_type = state.input_type

    if not os.path.exists(source_path):
        raise FileNotFoundError(f"File not found: {source_path}")

    if source_type == "text":
        with open(source_path, "r", encoding="utf-8") as f:
            content = f.read()
    elif source_type == "pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(source_path)
        content = "\n".join([page.extract_text() for page in reader.pages])
    else:
        raise ValueError("Unsupported source type")

    print("[✅] Parsed Input Content")
    return AgentState(
        input_path=source_path,
        input_type=source_type,
        parsed_content=content
    )
