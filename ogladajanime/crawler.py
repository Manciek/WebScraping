import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunsplit, urlsplit
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml",
    "Accept-Language": "en-GB,en-US,en,pl",
    "Referer": "https://www.google.com"
}

s = requests.session()
s.headers.update(headers)
s.get("https://google.com")

# Site to target/ base
site = "https://ogladajanime.pl"

# Real thing
def StartCrawlingURLS(target, session: requests.Session):
    result: set[str] = set()
    urls: set[str] = {target}
    while urls:
        target_site = urls.pop()
        print("Trying: ", target_site)
        # Try if Network Error then move on
        try:
            r = session.get(target_site, timeout=3)
            if not r.ok:
                continue
        except requests.exceptions.RequestException:
            continue

        soup = BeautifulSoup(r.text, features='lxml')
        hrefs = [a["href"] for a in soup.find_all("a") if a.get("href")]
        # Parse urls (normalize them)
        for url in hrefs:
            joined = urljoin(target_site, url)
            sp = urlsplit(joined)
            clean = urlunsplit((sp.scheme, sp.netloc, sp.path, "", ""))
            if clean not in result and urlparse(clean).netloc == urlparse(target).netloc:
                urls.add(clean)
        result.add(target_site)
    return result

def ProcessResultURLS(results: set[str], target):
    ds = pd.DataFrame(results, columns=["URLS"])
    ds.to_csv(f"{target}_urls.csv", index=False, sep=";")

res = StartCrawlingURLS(site, s)
ProcessResultURLS(res, "ogladajanime.pl")
