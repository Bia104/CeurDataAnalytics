import pdfplumber
import logging

import release.parser.parser as parser
import release.models.paper_info as models

pdf_path = "../resources/paos2017_paper1.pdf"
pdf_p1v3901_path = "../resources/p1v3901.pdf"
pdf_p1v3970_path = "../resources/p1v3970.pdf"
pdf_p29v3896_path = "../resources/p29v3896.pdf"
def test_get_keywords():
    
    with pdfplumber.open(pdf_path) as pdf:
        keywords = parser.get_keywords(pdf)
    
    assert isinstance(keywords, list), "The keywords must be a list"
    assert len(keywords) > 0, "The list of keywords must not be empty"
    assert "DBpedia" in keywords, "The keyword 'DBpedia' should be present"

def test_get_references_correct_number():
    with pdfplumber.open(pdf_path) as pdf:
        references = parser.get_references(pdf)
    assert isinstance(references, list), "The references must be a list"
    assert len(references) > 0, "The list of references must not be empty"
    assert len(references) == 15, "The list of references must contain 15 elements"

def test_get_references_correct_format():
    with pdfplumber.open(pdf_path) as pdf:
        references = parser.get_references(pdf)
    assert isinstance(references, list), "The references must be a list"
    assert len(references) == 15, "The list of references must contain 15 elements"

    for i in range(len(references)):
        reference = references[i]
        assert isinstance(reference, models.RelatedPaperInfo), "The references must be of 'RelatedPaperInfo' type"
        assert hasattr(reference, "title"), "The referenced must have a 'title' attribute"
        assert hasattr(reference, "authors"), "The referenced must have a 'authors' attribute"
        assert hasattr(reference, "text"), "The referenced must have a 'text' attribute"

        assert reference.text.startswith(f"{i + 1}.")

def test_get_references_correct_authors():
    with pdfplumber.open(pdf_path) as pdf:
        references = parser.get_references(pdf)
    assert isinstance(references, list), "The references must be a list"
    assert len(references) == 15, "The list of references must contain 15 elements"
    reference = references[1]
    assert isinstance(reference, models.RelatedPaperInfo), "The references must be of 'RelatedPaperInfo' type"
    assert hasattr(reference, "title"), "The referenced must have a 'title' attribute"
    assert hasattr(reference, "authors"), "The referenced must have a 'authors' attribute"
    assert hasattr(reference, "text"), "The referenced must have a 'text' attribute"
    assert len(reference.authors) == 3, "The referenced must have 3 authors"

def test_get_reference_2_correct_title():
    with pdfplumber.open(pdf_path) as pdf:
        references = parser.get_references(pdf)
    assert isinstance(references, list), "The references must be a list"
    assert len(references) == 15, "The list of references must contain 15 elements"
    reference = references[1]
    assert isinstance(reference, models.RelatedPaperInfo), "The references must be of 'RelatedPaperInfo' type"
    assert hasattr(reference, "title"), "The referenced must have a 'title' attribute"
    assert hasattr(reference, "authors"), "The referenced must have a 'authors' attribute"
    assert hasattr(reference, "text"), "The referenced must have a 'text' attribute"
    assert reference.title == "RDFization of Japanese Electronic Dictionaries and LOD", "The title of the reference 2 is incorrect"

def test_parse_p1v3901():
    paper_info = parser.parse_file_path(pdf_p1v3901_path)

    assert len(paper_info.keywords) == 5
    assert paper_info.keywords == ["Social Chatbots", "Privacy Policies", "Ethics", "Al Companions", "Data Protection"]

    assert len(paper_info.related_papers) == 40

    for i in range(len(paper_info.related_papers)):
        assert isinstance(paper_info.related_papers[i], models.RelatedPaperInfo), "The references must be of 'RelatedPaperInfo' type"
        assert hasattr(paper_info.related_papers[i], "title"), "The referenced must have a 'title' attribute"
        assert hasattr(paper_info.related_papers[i], "authors"), "The referenced must have a 'authors' attribute"
        assert hasattr(paper_info.related_papers[i], "text"), "The referenced must have a 'text' attribute"
        assert paper_info.related_papers[i].text[:len(str(i + 1)) + 2] == f"[{i + 1}]", f"The text of the reference is incorrect: {paper_info.related_papers[i].text[:10]} != [{i + 1}]."

    reference_1 = paper_info.related_papers[0]
    assert  reference_1.authors == ["M.-H. Huang", "R. Rust", "V. Maksimovic"], "The authors of the reference 1 are incorrect"
    assert reference_1.title == "The Feeling Economy: Managing in the Next Generation of Artificial Intelligence (Al), California Management Review 61(4) (2019) 43-65"

def test_parse_p1v3970():
    parser_info = parser.parse_file_path(pdf_p1v3970_path)

    assert isinstance(parser_info, models.PaperInfo), "The parser info must be of 'PaperInfo' type"
    assert len(parser_info.keywords) == 6, "The number of keywords must be 5"
    assert len(parser_info.related_papers) != 0, "The number of related papers must not be 0"
    assert len(parser_info.related_papers) == 29 , "The number of related papers must be 29"

def test_parse_p29v3896():
    paper_info = parser.parse_file_path(pdf_p29v3896_path)

    assert isinstance(paper_info, models.PaperInfo), "The parser info must be of 'PaperInfo' type"
    assert len(paper_info.keywords) == 11, "The number of keywords must be 7"

def test_parse_p12v3941():
    pdf_path = "../resources/p12v3941.pdf"
    paper_info = parser.parse_file_path(pdf_path)

    assert isinstance(paper_info, models.PaperInfo), "The parser info must be of 'PaperInfo' type"
    assert len(paper_info.related_papers) == 40, "The number of related papers must be 20"