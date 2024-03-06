import urllib.request
from pathlib import Path

import bs4

base_url = "http://redstone.logickorea.co.kr"
res = urllib.request.urlopen(
    "http://redstone.logickorea.co.kr/notice/noticeboard/view.aspx?sqn=7231"
)
soup = bs4.BeautifulSoup(res.text)

top = soup.select_one("#board_notice_view .post")
if top is None:
    raise ValueError

c = 0
for i in top.select("img"):
    src_url = i.attrs["src"]
    if src_url[0:15] == "data:image/png;":
        r = urllib.request.urlopen(src_url)  # noqa: S310
        dst = f"out/img/{c}.png"
        i.attrs["src"] = f"img/{c}.png"
        with open(dst, "wb") as f:
            f.write(r.file.read())
        c += 1
    elif src_url[0] == "/":
        r = urllib.request.urlopen(base_url + src_url)  # noqa: S310
        name = Path(src_url).name
        dst = f"out/img/{name}"
        i.attrs["src"] = f"img/{name}"
        with open(dst, "wb") as f:
            f.write(r.read())
    else:
        # fallback
        print(i.attrs["src"][0:80])

with open("out/index.html", "w", encoding="utf-8") as f:
    f.write(str(top))
