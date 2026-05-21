import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9,pl;q=0.8",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://ogladajanime.pl"}

session = requests.session()
strony = ['https://ogladajanime.pl/all_anime_list/']

main = strony.pop()
r = session.get(main, headers=headers, allow_redirects=True)
r.encoding = "utf-8"
soup = BeautifulSoup(r.text, 'lxml')

a_s = soup.select("a.btn.btn-primary.mt-2.mr-1.p-1.px-2")
hrefs = [f"https://ogladajanime.pl{a.get('href')}" for a in a_s]
#Double navigation
strony = hrefs[0:len(hrefs)//2]

anime_link_dict: defaultdict[str, list[tuple[str, str]]] = defaultdict(list)
while strony:
    # Pop page
    # Find all anime title: link
    # Add to dict, move on
    current = strony.pop()
    r = session.get(current, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(r.text, 'lxml').select_one("body")

    znak = current[-1]
    anime_a_s = soup.select("a.tooltip.tooltip-anime.text-bold")

    for anime in anime_a_s:
        title = anime.text.strip().removeprefix("\u2022").strip()
        link = f"https://ogladajanime.pl{anime.get('href')}"
        anime_link_dict[znak].append((title, link))


data = [(znak.upper(), tytul, url)
         for znak, animes in anime_link_dict.items()
         for tytul, url in animes]


sheet = pd.DataFrame(data, columns=["Znak", "Title", "Url"])
sheet.to_csv("anime_list.csv", index=False, sep=";")
