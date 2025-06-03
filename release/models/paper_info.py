class RelatedPaperInfo:
    def __init__(self, title: str, authors: list[str], text: str):
        self.title = title
        self.authors = authors
        self.text = text
    def __str__(self):
        return f"Title: {self.title}, Authors: {', '.join(self.authors)}, Text: {self.text}"


class PaperInfo:
    def __init__(self, keywords: list[str], related_papers : list[RelatedPaperInfo]):
        self.keywords = keywords
        self.related_papers = related_papers

    def to_dict(self):
        return {
            'keywords': self.keywords,
            'related_papers': [paper.__dict__ for paper in self.related_papers]
        }
        