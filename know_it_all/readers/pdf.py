import fitz

# This function will extract and return the pdf file text content.
def extract_pdf_text(filePath=''):

    # Open the pdf file in read binary mode.
    with fitz.open(filePath) as doc:
        text=""
        for page in doc:
            text+=page.getText()
    return text


def to_text(path):
    return extract_pdf_text(path)

if __name__=="__main__":
    pdf_file_path=r"C:\code\memory_palace\data\The Odyssey.pdf"
    pdf_text = extract_pdf_text(pdf_file_path)
    print(pdf_text)
    with open("data/The_Odyssey.txt",
              'w',encoding="utf-8") as f:
              f.write(pdf_text)
    #text="\n".join(pdf_text)
    #with open("C:\code\memory_palace\data\9780470276808-Chapter-1-Cluster-analysis_epub.txt",'w',encoding="utf-8") as f:
    #    f.write(text)