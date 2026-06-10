import PyPDF2


def extract_text_from_pdf(pdf_file):

    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


def get_pdf_statistics(text):

    words = len(text.split())

    characters = len(text)

    lines = len(text.split("\n"))

    return {
        "Words": words,
        "Characters": characters,
        "Lines": lines
    }