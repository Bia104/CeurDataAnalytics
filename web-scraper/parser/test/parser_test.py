

import pdfplumber
from parser.parser import get_keywords, get_references
import logging
import models.papaer_info as models
pdf_path = "parser/test/resources/paos2017_paper1.pdf"

def test_get_keywords():
    
    with pdfplumber.open(pdf_path) as pdf:
        keywords = get_keywords(pdf)
    
    assert isinstance(keywords, list), "Le parole chiave devono essere una lista"
    assert len(keywords) > 0, "La lista delle parole chiave non deve essere vuota"
    assert "DBpedia" in keywords, "La parola chiave 'DBpedia' dovrebbe essere presente"

def test_get_references_correct_number():
    with pdfplumber.open(pdf_path) as pdf:
        references = get_references(pdf)
    assert isinstance(references, list), "Le referenze devono essere una lista"
    assert len(references) > 0, "La lista delle referenze non deve essere vuota"
    assert len(references) == 15, "La lista delle referenze deve contenere 15 elementi"

def test_get_references_correct_format():
    with pdfplumber.open(pdf_path) as pdf:
        references = get_references(pdf)
    assert isinstance(references, list), "Le referenze devono essere una lista"
    
    for i in range(len(references)):
        reference = references[i]
        assert isinstance(reference, models.RelatedPaperInfo), "Le referenze devono essere di tipo RelatedPaperInfo"
        assert hasattr(reference, "title"), "Le referenze devono avere un attributo 'title'"
        assert hasattr(reference, "authors"), "Le referenze devono avere un attributo 'authors'"
        assert hasattr(reference, "text"), "Le referenze devono avere un attributo 'text'"

        assert reference.text.startswith(f"{i + 1}.")

