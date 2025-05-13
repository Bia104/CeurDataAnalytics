class PaperInfo : 
    def __init__(self, paper_id : str, title : str, authors : list[str], keywords: list[str], abstract : str, related_papers : list[str]):
        self.paperId = paper_id
        self.title = title
        self.authors = authors
        self.keywords = keywords
        self.abstract = abstract
        self.related_papers = related_papers

class RelatedPaperInfo:
    def __init__(self, title: str, authors: list[str], text: str):
        self.title = title
        self.authors = authors
        self.text = text
    def __str__(self):
        return f"Title: {self.title}, Authors: {', '.join(self.authors)}, Text: {self.text}"
        