genres = {
    # "action": "1",
    "adventure": "2",
    "comedy": "4",
    "demons": "6",
    "drama": "8",
    # "fantasy": "10",
    # "historical": "13",
    "romance": "22",
    "shounen": "27",
}
STORAGE_TYPE = "mongo"  # choices: ['mongo','file']


def crawl_link(genre_id):
    link = f"https://anime-list.net/anime/genre/{genre_id}/?page="
    return link


if __name__ == "__main__":
    pass
