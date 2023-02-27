from bs4 import BeautifulSoup


class AnimeDetailParser:
    def __init__(self):
        self.soup = None

    @property
    def title(self):

        div_tag = self.soup.find("div", attrs={"class": "header-single__info"})
        title_tag = div_tag.find("h1")
        if title_tag:
            return title_tag.text.strip()

    @property
    def summary(self):

        summary_tag = self.soup.find("p", attrs={"class": "story"})
        if summary_tag:
            return summary_tag.text.strip()

    @property
    def score(self):
        score_tag = self.soup.find("div", attrs={"class": "points__item points__item--numb"})
        if score_tag:
            return score_tag.text

    @property
    def genre(self):

        genre_span = self.soup.find('span', text='ژانرها')
        a_tags = genre_span.find_next_sibling('span').find_all('a')
        if a_tags:
            return [a.text for a in a_tags]

    def parser(self, html_doc):
        self.soup = BeautifulSoup(html_doc, "html.parser")
        data = dict(title=self.title, summary=self.summary, score=self.score, genre=self.genre)
        return data
