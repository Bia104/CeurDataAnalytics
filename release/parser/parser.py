'''
This module is used to parse a PDF file and extract keywords and references from it.
is part of the parsing for a single paper. You should insert into PaperInfo: title, authors, and this module will extract the keywords and references.
'''
import re

from release.models.paper_info import PaperInfo, RelatedPaperInfo
import base64
import pdfplumber
import enchant
from pdfplumber.pdf import PDF

from io import BytesIO

eng_dic = enchant.Dict("en_US")
eng_dic.add("Convolutional")
eng_dic.add("convolutional")
def parse_file_path(file_path: str) -> PaperInfo:
    with open(file_path, "rb") as file:
        return parse_file_base64(base64.b64encode(file.read()).decode())

def parse_file_bytes(file_bytes: bytes) -> PaperInfo:
    bytesIO_file : BytesIO = BytesIO(file_bytes)
    return parse_pdf(pdfplumber.open(bytesIO_file))

def parse_file_base64(base64_file: str) -> PaperInfo:
    bytes_file : bytes = base64.b64decode(base64_file)
    bytesIO_file : BytesIO = BytesIO(bytes_file)
    return parse_pdf(pdfplumber.open(bytesIO_file))

def parse_pdf(file: PDF) -> PaperInfo:
    keywords : list[str] = get_keywords(file)
    references : list[RelatedPaperInfo] = get_references(file)
    return PaperInfo(
        keywords = keywords,
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
                while j < len(words) and len(re.sub(r"[^A-Za-z]", "", words[j]["text"])) == 0:
                    j = j + 1
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
            or word["text"].lower() == "reference"
            or word["text"].lower() == "reference:"
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

        reference_text_words = reference_text.split()
        count_eng_words = 0
        start_title = 0
        threshold = 5
        while threshold >= 2:
            count_eng_words = 0
            for i in range(len(reference_text_words)):
                word = reference_text_words[i].strip()
                clean_word = re.sub(r"[^a-zA-Z\-]", "", word)
                if len(clean_word) > 0 and (not (clean_word.isupper() and word.replace(',', "")[-1] == '.' or len(
                        [dot for dot in word if word == '.']) > 1)) and eng_dic.check(clean_word):
                    count_eng_words += 1
                else:
                    count_eng_words = 0
                if count_eng_words >= threshold:
                    start_title = i - count_eng_words + 1
                    break
            if count_eng_words >= threshold:
                break
            threshold -= 1

        authors_words = reference_text_words[1:start_title]

        for i, word in enumerate(authors_words):
            if ":" in word or ";" in word or ("." in word and not (re.match(r"[A-Z]\.", word))):
                start_title = start_title - len(authors_words) + i + 1
                authors_words = authors_words[:start_title]
                break
        if "and" in authors_words:
            authors_words.remove("and")
        if "&" in authors_words:
            authors_words.remove("&")
        authors_text = " ".join(authors_words)
        authors_list = authors_text.split(",")
        authors_list = [author.strip() for author in authors_list if author.strip()]
        # try to assume the correct separator for the title
        title_part = " ".join(reference_text_words[start_title:])
        first_semi = title_part.find(";")
        first_dot = title_part.find(".")
        if first_semi != -1 and (first_dot == -1 or first_semi < first_dot):
            title_part = title_part[:first_semi]
        elif first_dot != -1:
            title_part = title_part[:first_dot]
        return authors_list, title_part
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