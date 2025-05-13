from release.models.paper_info import PaperInfo, RelatedPaperInfo
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



def get_keywords(pdf: PDF) -> list[any]:
    keywords = []
    
    for page in pdf.pages:
        words = page.extract_words(extra_attrs=["fontname", "size"])
        for i in range(len(words)):
            keyword = words[i]
            if _check_if_is_keyword(keyword):
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

def _get_references_words(pdf: PDF) -> list[any]:
    references = []
    for page in pdf.pages:
        words = page.extract_words(extra_attrs=["fontname", "size"])
        for i in range(len(words)):
            reference = words[i]
            if _check_if_is_reference(reference):
                references = []
                j = i + 1
                first_word_size = words[j]["size"]
                while j < len(words) and not _check_size_changed(words[j], first_word_size):
                    references.append(words[j])
                    j += 1
                return references

def _check_if_is_keyword(word) -> bool:
    return ((
            word["text"].lower() == "keywords" 
            or word["text"].lower() == "keywords:"
        )
        and _check_if_is_bold(word["fontname"])
    )

def _check_if_is_bold(fontname : str) -> bool:
    return "Bold" in fontname or "CMB"  in fontname

def _check_if_is_reference(word) -> bool:
    return ((
            word["text"].lower() == "references" 
            or word["text"].lower() == "references:"
        )
        and _check_if_is_bold(word["fontname"])
    )

def get_references(pdf: PDF) -> list[RelatedPaperInfo]:
    import re

    def split_words(words: list[any]) -> list[list[any]]:
        if not words:
            return []

        references = []
        current_reference = []
        separator_pattern = r"\d+\."
        for i in range(len(words)):
            word = words[i]
            if re.match(separator_pattern, word["text"]) and (i > 0 or _check_new_line(word, words[i - 1])):
                if current_reference:
                    references.append(current_reference)
                current_reference = [word]
            else:
                current_reference.append(word)

        if current_reference:
            references.append(current_reference)

        return references

    def extract_authors_and_title(reference_text: str) -> tuple[list[str], str]:
        author_pattern = r"[A-Z][a-z]+(?: [A-Z][a-z]+)*"
        
        parts = reference_text.split(",")
        authors = []
        title_start_index = 0

        for i, part in enumerate(parts):
            if re.fullmatch(author_pattern, part.strip()):
                authors.append(part.strip())
            else:
                title_start_index = i
                break

        title = ", ".join(parts[title_start_index:]).strip()
        return authors, title

    words = _get_references_words(pdf)
    references = split_words(words)

    related_papers = []
    for reference in references:
        full_text = " ".join(word["text"] for word in reference)
        authors, title = extract_authors_and_title(full_text)
        related_paper = RelatedPaperInfo(title=title, authors=authors, text=full_text)
        related_papers.append(related_paper)

    return related_papers

def _check_size_changed(word, first_word_size, epsilon = 0.1) -> bool:
    return abs(word["size"] - first_word_size) > epsilon

def _check_new_line(word, previous_word) -> bool:
    return abs(word["top"] - previous_word["top"]) > 0.1 and abs(word["bottom"] - previous_word["bottom"]) > 0.1