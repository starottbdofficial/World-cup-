import requests
import datetime
import re

# সোর্স লিঙ্ক
JSON_URLS = [
    "https://raw.githubusercontent.com/srhady/bingstream/refs/heads/main/playlist.json",
    "https://raw.githubusercontent.com/srhady/data/refs/heads/main/playlist.json"
]
M3U_SOURCES = [
    "https://raw.githubusercontent.com/sm-monirulislam/AynaOTT-auto-update-playlist/refs/heads/main/AynaOTT.m3u",
    "https://iptv-org.github.io/iptv/index.m3u"
]

FALLBACK_VIDEO = "https://raw.githubusercontent.com/ibstvofficial/IBS-TV-special-movies.m3u/refs/heads/main/1777291577865.mp4"
FALLBACK_LOGO = "https://camo.githubusercontent.com/93929647baabb50606ccf95056c8ff42b3f2f9249c5364fa1e0f8b7dcef395f3/68747470733a2f2f626469786970747662642e636f6d2f6c6f676f2e706e67"

# আপনার কাঙ্ক্ষিত ক্যাটাগরি অর্ডার
ORDERED_CATEGORIES = ["FIFA World cup", "Sports", "Bangladesh", "Kolkata", "India", "Kids", "Movie", "Music"]

def get_category(name, group):
    name_up = name.upper()
    if any(x in name_up for x in ["SOMOY", "BTV", "T SPORTS", "FIFA"]):
        return "FIFA World cup"
    
    mapping = {
        "Sports": ["SPORTS", "CRICKET", "FOOTBALL"],
        "Bangladesh": ["BD", "BANGLA", "DHAKA"],
        "Kolkata": ["KOLKATA", "WB"],
        "India": ["INDIA", "HINDI", "STAR"],
        "Kids": ["KIDS", "CARTOON"],
        "Movie": ["MOVIE", "FILM"],
        "Music": ["MUSIC"]
    }
    for cat, keywords in mapping.items():
        if any(k in name_up for k in keywords): return cat
    return "Other"

def fetch_and_process():
    channels = []
    
    # JSON সোর্স
    for url in JSON_URLS:
        try:
            data = requests.get(url, timeout=10).json()
            items = data.get("channels", data.get("matches", []))
            for item in items:
                name = item.get("channel_name", item.get("Match Title", "Unknown"))
                url = item.get("stream_url", item.get("Stream URL", FALLBACK_VIDEO))
                if isinstance(url, list): url = url[0].get("play_url") if isinstance(url[0], dict) else url[0]
                channels.append({"name": name, "group": get_category(name, ""), "logo": item.get("logo_url", FALLBACK_LOGO), "url": url or FALLBACK_VIDEO})
        except: continue

    # M3U সোর্স (iptv-org সহ)
    for m3u_url in M3U_SOURCES:
        try:
            resp = requests.get(m3u_url, timeout=15).text
            for match in re.finditer(r'#EXTINF:-1 tvg-logo="(.*?)".*?group-title="(.*?)".*?,(.*?)\n(.*?)\n', resp):
                logo, group, name, url = match.groups()
                cat = get_category(name, group)
                if cat != "Other": # শুধু আপনার প্রয়োজনীয় ক্যাটাগরি গুলোই যুক্ত হবে
                    channels.append({"name": name, "group": cat, "logo": logo, "url": url})
        except: continue
    return channels

def write_m3u(channels):
    with open("FIFA-world-cup-4k.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("# Playlist update dates and times: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        f.write("# Playlist owner: STAR OTT BD\n# Playlist Creator: MD shakib Hasan\n")
        f.write("# What's app: +8801610598422\n# Telegram: https://t.me/ibstvbdn")
        f.write("# Our official partner : IBS TV. STAR SHARE. OPPLEX.\n\n")

        # সর্টিং ও ফিল্টারিং
        channels.sort(key=lambda x: ORDERED_CATEGORIES.index(x['group']) if x['group'] in ORDERED_CATEGORIES else 99)

        for ch in channels:
            f.write(f'#EXTINF:-1 tvg-logo="{ch["logo"]}" group-title="{ch["group"]}",{ch["name"]}\n{ch["url"]}\n')

if __name__ == "__main__":
    write_m3u(fetch_and_process())
    
