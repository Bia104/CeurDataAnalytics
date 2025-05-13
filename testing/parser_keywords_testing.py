import pdfplumber
import logging

from release.parser.parser import get_keywords, get_references
import release.models.paper_info as models

pdf_path = "parser/test/resources/paos2017_paper1.pdf"

def test_get_keywords():
    
    with pdfplumber.open(pdf_path) as pdf:
        keywords = get_keywords(pdf)
    
    assert isinstance(keywords, list), "The keywords must be a list"
    assert len(keywords) > 0, "The list of keywords must not be empty"
    assert "DBpedia" in keywords, "The keyword 'DBpedia' should be present"

def test_get_references_correct_number():
    with pdfplumber.open(pdf_path) as pdf:
        references = get_references(pdf)
    assert isinstance(references, list), "The references must be a list"
    assert len(references) > 0, "The list of references must not be empty"
    assert len(references) == 15, "The list of references must contain 15 elements"

def test_get_references_correct_format():
    with pdfplumber.open(pdf_path) as pdf:
        references = get_references(pdf)
    assert isinstance(references, list), "The references must be a list"
    
    for i in range(len(references)):
        reference = references[i]
        assert isinstance(reference, models.RelatedPaperInfo), "The references must be of 'RelatedPaperInfo' type"
        assert hasattr(reference, "title"), "The referenced must have a 'title' attribute"
        assert hasattr(reference, "authors"), "The referenced must have a 'authors' attribute"
        assert hasattr(reference, "text"), "The referenced must have a 'text' attribute"

        assert reference.text.startswith(f"{i + 1}.")

