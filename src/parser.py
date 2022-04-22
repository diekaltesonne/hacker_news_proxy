from bs4 import BeautifulSoup as bs
import re

blacklist = ["script", "noscript", "style", "code" "meta", "link"]


def filter(text):
    return re.sub(r"\b([а-яёa-z-]{6})\b", r"\1™", text, flags=re.IGNORECASE)


def parse_html(context_data, url):
    soup = bs(context_data, "lxml")
    for a in soup.findAll("a", href=True):
        a["href"] = a["href"].replace("https://news.ycombinator.com", url)

    for el in soup.find_all(text=True):
        text = el.string
        if text and False not in [el.find_parent(x) is None for x in blacklist]:
            el.replace_with(filter(text))
    return str(soup)
