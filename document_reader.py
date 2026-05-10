def read_txt(file):
    return file.read().decode("utf-8", errors="ignore")


def read_pdf(file):
    import fitz  # PyMuPDF

    pdf_bytes = file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""
    for page in doc:
        text += page.get_text("text") + "\n\n"

    return text


def read_docx(file):
    from docx import Document

    doc = Document(file)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])


def read_eml(file):
    import mailparser

    mail = mailparser.parse_from_bytes(file.read())

    subject = mail.subject or ""
    sender = mail.from_[0][1] if mail.from_ else ""
    receiver = mail.to[0][1] if mail.to else ""
    body = mail.body or ""

    return f"""
Subject: {subject}
From: {sender}
To: {receiver}

{body}
"""


def clean_text(text):
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if line:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def read_uploaded_file(file):
    file_type = file.name.split(".")[-1].lower()

    if file_type == "txt":
        text = read_txt(file)
    elif file_type == "pdf":
        text = read_pdf(file)
    elif file_type == "docx":
        text = read_docx(file)
    elif file_type == "eml":
        text = read_eml(file)
    else:
        text = ""

    return clean_text(text)