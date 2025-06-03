from release.models.paper_info import PaperInfo
class Paper:
    def __init__(self, url, title, pages, author, volume_id=None):
        self.paper_info = None
        self.url = url
        self.title = title
        self.pages = pages
        self.author = author
        self.volume_id = volume_id

    def add_paper_info(self, paper_info: PaperInfo):
        self.paper_info = paper_info

    def to_dict(self):
        return {
            'url': self.url,
            'title': self.title,
            'pages': self.pages,
            'author': self.author,
            'volume_id': self.volume_id,
            'paper_info': self.paper_info.to_dict() if self.paper_info else None
        }