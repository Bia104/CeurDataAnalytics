

import pdfplumber
from parser.parser import get_keywords

def test_get_keywords():
    pdf_path = "parser/test/resources/paos2017_paper1.pdf"
    
    with pdfplumber.open(pdf_path) as pdf:
        keywords = get_keywords(pdf)
    
    assert isinstance(keywords, list), "Le parole chiave devono essere una lista"
    assert len(keywords) > 0, "La lista delle parole chiave non deve essere vuota"
    assert "DBpedia" in keywords, "La parola chiave 'DBpedia' dovrebbe essere presente"