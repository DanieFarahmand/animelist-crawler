from bs4 import BeautifulSoup


class AnimeDetailParser:

    def parser(self, html_doc):
        soup = BeautifulSoup(html_doc, "html.parser")
        data = dict(title=None, summary=None, score=0)

        div_tag = soup.find("div", attrs={"class": "header-single__info"})
        title_tag = div_tag.find("h1")
        if title_tag:
            data["title"] = title_tag.text.strip()

        summary_tag = soup.find("p", attrs={"class": "story"})
        if summary_tag:
            data["summary"] = summary_tag.text.strip()

        score_tag = soup.find("div", attrs={"class": "points__item points__item--numb"})
        if score_tag:
            data["score"] = score_tag.text

        return data
