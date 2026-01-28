import fitz
def extract_text(filepath):
    doc = fitz.open(filepath)
    text=""
    for page in doc:
        text+=page.get_text()
    doc.close()
    return text    