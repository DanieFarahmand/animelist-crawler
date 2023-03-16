from bs4 import BeautifulSoup


class AnimeDetailParser:
    """
    A class that get the elements form a web page
    """

    def __init__(self):
        self.soup = None

    @property
    def title(self):
        div_tag = self.soup.find("div", attrs={"class": "header-single__info"})
        title_tag = div_tag.find("h1")

        title_tag = div_tag.find("h1")
        # if title_tag exists, return its text with leading/trailing whitespace removed
        # and any colons replaced with hyphens.
        if title_tag:
            return title_tag.text.strip().replace(":", "-")

    @property
    def summary(self):
        summary_tag = self.soup.find("p", attrs={"class": "story"})
        # if summary_tag exists, return its text with leading/trailing whitespace removed
        if summary_tag:
            return summary_tag.text.strip()

    @property
    def score(self):
        score_tag = self.soup.find("div", attrs={"class": "points__item points__item--numb"})
        # if score_tag exists, return its text
        if score_tag:
            return score_tag.text

    @property
    def image(self):
        img_tag = self.soup.find("img", attrs={"class": "poster"})
        # return a dictionary with the URL of the image and a flag indicating whether it has been downloaded or not
        return {"url": "https://anime-list.net" + img_tag["src"], "flag": False}

    @property
    def genre(self):
        genre_span = self.soup.find('span', text='ژانرها')
        a_tags = genre_span.find_next_sibling('span').find_all('a')
        # if a_tags exist, return a list of their text
        if a_tags:
            return [a.text for a in a_tags]

    @property
    def subtitle(self):
        subtitles_box = self.soup.find("div", attrs={"cLass": "row p18 ltr"})
        if subtitles_box:
            subtitle_a_tags = subtitles_box.find_all("a", attrs={"class": "item__link"})
            if subtitle_a_tags:
                print(subtitles_box)
                return [sub_link.get("href") for sub_link in subtitle_a_tags]
            else:
                return []

    def parser(self, html_doc):
        # parse the HTML document and store the resulting soup object in the instance variable soup
        self.soup = BeautifulSoup(html_doc, "html.parser")
        # create a dictionary with the anime's title, image, summary, score, and genre
        data = dict(title=self.title, image=self.image, summary=self.summary, score=self.score, genre=self.genre,
                    subtitle=self.subtitle)
        return data
