'''
This module is used to parse a PDF file and extract keywords and references from it.
is part of the parsing for a single paper. You should insert into PaperInfo: title, authors, and this module will extract the keywords and references.
'''
from release.models.paper_info import PaperInfo, RelatedPaperInfo
import base64
import pdfplumber
from pdfplumber.pdf import PDF

from io import BytesIO

def parse_file_path(file_path : str, info : PaperInfo) -> PaperInfo:
    with open(file_path, "rb") as file:
        return parse_file_base64(base64.b64encode(file.read()).decode(), info)

def parse_file_base64(base64_file : str, info : PaperInfo) -> PaperInfo:
    bytes_file : bytes = base64.b64decode(base64_file)
    bytesIO_file : BytesIO = BytesIO(bytes_file)
    return parse_pdf(pdfplumber.open(bytesIO_file), info)

def parse_pdf(file : PDF, info : PaperInfo) -> PaperInfo:
    keywords : list[str] = get_keywords(file)
    references : list[RelatedPaperInfo] = get_references(file)
    return PaperInfo(
        paper_id = info.paperId,
        title = info.title,
        authors = info.authors,
        keywords = keywords,
        abstract = info.abstract,
        related_papers = references
    )




def get_keywords(pdf: PDF) -> list[str]:
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
                    keywords = text.replace("$-$", " ").split(",")
                else:
                    keywords = text.split("$-$")
                keywords = [k.strip() for k in keywords if k.strip()]
                return keywords
    return keywords

def _get_references_words(pdf: PDF) -> list[str]:
    references = []
    for page in pdf.pages:
        words = page.extract_words(extra_attrs=["fontname", "size"])
        for i in range(len(words)):
            reference = words[i]
            if _check_if_is_reference(reference):
                actual_page = page
                references = []
                j = i + 1
                first_word_size = words[j]["size"]
                while(j < len(words)
                      and (
                          not _check_size_changed(words[j], first_word_size)
                          or _check_if_is_superscript_or_subscript(words[j])
                      )
                ) :
                    references.append(words[j])
                    j += 1
                    if j >= len(words) and pdf.pages.index(actual_page) + 1 < len(pdf.pages):
                        actual_page = pdf.pages[pdf.pages.index(actual_page) + 1]
                        words = actual_page.extract_words(extra_attrs=["fontname", "size"])
                        j = 0

                return references
    return []


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
        separator_pattern = r"^(\d+\.)|\[\d+\]"
        for i in range(len(words)):
            word = words[i]
            if re.match(separator_pattern, word["text"]) and (i > 0 and _check_new_line(word, words[i - 1])):
                if current_reference:
                    references.append(current_reference)
                current_reference = [word]
            else:
                current_reference.append(word)

        if current_reference:
            references.append(current_reference)

        return references

    def extract_authors_and_title(reference_text: str) -> tuple[list[str], str]:

        title_separators = [":", ";", "."]
        # Try to find the first separator in the reference text
        for sep in title_separators:
            if sep in reference_text:
                parts = reference_text.split(sep, 1)
                authors_part = parts[0]
                break
        else:
            # Is not a recognizable reference
            authors_part = reference_text
            parts = [authors_part]
        title_part = "".join(parts[1:]).strip() if len(parts) > 1 else ""

        authors = []
        for author in authors_part.split(","):
            if "and" in author:
                authors.extend([a.strip() for a in author.split("and")])
            else:
                authors.append(author.strip())

        authors = [a for a in authors if a]
        authors = [re.sub(r"(?<=[a-z])(?=[A-Z])", " ", a) for a in authors]
        # try to assume the correct separator for the title
        first_semi = title_part.find(";")
        first_dot = title_part.find(".")
        if first_semi != -1 and (first_dot == -1 or first_semi < first_dot):
            title_part = title_part[:first_semi]
        elif first_dot != -1:
            title_part = title_part[:first_dot]
        return authors, title_part
    words = _get_references_words(pdf)
    references = split_words(words)

    related_papers = []
    for reference in references:
        full_text = " ".join(word["text"] for word in reference)
        authors, title = extract_authors_and_title(full_text)
        related_paper = RelatedPaperInfo(title=title, authors=authors, text=full_text)
        related_papers.append(related_paper)

    return related_papers

def _check_size_changed(word, first_word_size, epsilon = 1) -> bool:
    return abs(word["size"] - first_word_size) > epsilon

def _check_new_line(word, previous_word) -> bool:
    return abs(word["top"] - previous_word["top"]) > 0.1 and abs(word["bottom"] - previous_word["bottom"]) > 0.1

def _check_if_is_superscript_or_subscript(word) -> bool:
    return word["upright"]