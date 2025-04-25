class PaperInfo : 
    def __init__(self, paperId : str, title : str, authors : list[str], keywords: list[str], abstract : str, related_papers : list[str]):
        self.paperId = paperId
        self.title = title
        self.authors = authors
        self.keywords = keywords
        self.abstract = abstract
        self.related_papers = related_papers

    
        