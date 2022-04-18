from encodings import utf_8
from bs4 import BeautifulSoup as bs
import re

blacklist = [
    "meta",
    "script",
]


def filter(text):
    return re.sub(r"\b([а-яёa-z-]{6})\b", r"\1™", text, flags=re.IGNORECASE)


def parse_html(context_data):
    soup = bs(context_data, "html5lib")
    for el in soup.find_all(text=True):
        text = el.string
        if text and False not in [el.find_parent(x) is None for x in blacklist]:
            el.replace_with(filter(text))
    return soup.prettify()
