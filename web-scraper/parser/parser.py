from models.papaer_info import PaperInfo
import base64
import pdfplumber
from pdfplumber.pdf import PDF
from io import BytesIO
def parse_file_path(file_path : str) -> PaperInfo:
    with open(file_path, "rb") as file:
        return parse_file_base64(base64.b64encode(file.read()).decode())

def parse_file_base64(base64_file : str) -> PaperInfo:
    bytes_file : bytes = base64.b64decode(base64_file)
    bytesIO_file : BytesIO = BytesIO(bytes_file)
    return parse_pdf(pdfplumber.open(bytesIO_file))

def parse_pdf(file : PDF) -> PaperInfo:
    first_page = file.pages[0]
    title = first_page.filter(lambda obj: obj["object_type"] == "char" and ("Bold" in obj["fontname"]))[0]
    keywords : list[str] = get_keywords(file)



def get_keywords(pdf: PDF) -> list[str]:
    keywords = []
    
    for page in pdf.pages:
        words = page.extract_words(extra_attrs=["fontname", "size"])
        for i in range(len(words)):
            keyword = words[i]
            if check_if_is_keyword(keyword):
                j = i + 1
                first_word_size = words[j]["size"]
                text = ""
                while j < len(words) and words[j]["size"] == first_word_size:
                    text += words[j]["text"] + "$-$"
                    j += 1
                
                if "," in text:
                    keywords = text.strip("$-$").split(",")
                else:
                    keywords = text.strip().split("$-$")
                return keywords
    return keywords
def check_if_is_keyword(word) -> bool:
    return ((
            word["text"].lower() == "keywords" 
            or word["text"].lower() == "keywords:"
        )
        and (
          "Bold" in word["fontname"]
           or "CMBX9" in word["fontname"]       
        )
    )