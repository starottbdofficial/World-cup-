import requests
import datetime
import re

# সোর্স লিঙ্ক
M3U_SOURCES = {
    "Ayna": "https://raw.githubusercontent.com/sm-monirulislam/AynaOTT-auto-update-playlist/refs/heads/main/AynaOTT.m3u",
    "IPTVOrg": "https://iptv-org.github.io/iptv/index.m3u",
    "Akash": "https://raw.githubusercontent.com/srhady/Hady/refs/heads/main/akash_live.m3u"
}

FALLBACK_VIDEO = "https://raw.githubusercontent.com/ibstvofficial/IBS-TV-special-movies.m3u/refs/heads/main/1777291577865.mp4"
FALLBACK_LOGO = "https://camo.githubusercontent.com/93929647baabb50606ccf95056c8ff42b3f2f9249c5364fa1e0f8b7dcef395f3/68747470733a2f2f626469786970747662642e636f6d2f6c6f676f2e706e67"

# আপনার নির্ধারিত ক্যাটাগরি অর্ডার
ORDERED_CATEGORIES = ["FIFA World cup", "News", "Sports", "Bangladesh", "Music", "Kids", "Movie"]

def get_category(name, group):
    name_up = name.upper()
    
    # ১. FIFA World cup ক্যাটাগরি (BTV, SOMOY, T SPORTS, FIFA)
    if any(x in name_up for x in ["SOMOY", "BTV", "T SPORTS", "FIFA"]):
        return "FIFA World cup"
    
    # ২. অন্যান্য ক্যাটাগরি ম্যাপিং
    mapping = {
        "News": ["NEWS", "BBC", "CNN", "AL JAZEERA", "CHANNEL 24", "JOMUNA", "INDEPENDENT"],
        "Sports": ["SPORTS", "CRICKET", "FOOTBALL", "GOLF", "TEN"],
        "Bangladesh": ["BD", "BANGLA", "DHAKA", "CHANNEL I", "ATN"],
        "Music": ["MUSIC", "SONG", "GAAN"],
        "Kids": ["KIDS", "CARTOON", "NICK", "DISNEY", "POGO"],
        "Movie": ["MOVIE", "FILM", "HBO", "STAR MOVIES"]
    }
    
    for cat, keywords in mapping.items():
        if any(k in name_up for k in keywords):
            return cat
            
    return "Others"

def fetch_m3u(url):
    channels = []
    try:
        resp = requests.get(url, timeout=20).text
        # M3U পার্সিং
        for match in re.finditer(r'#EXTINF:-1 tvg-logo="(.*?)".*?group-title="(.*?)".*?,(.*?)\n(.*?)\n', resp):
            logo, group, name, url = match.groups()
            channels.append({"name": name, "group": get_category(name, group), "logo": logo, "url": url})
    except: pass
    return channels

def write_m3u(all_channels):
    with open("FIFA-world-cup-4k.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("# Playlist update dates and times: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        f.write("# Playlist owner: STAR OTT BD\n# Playlist Creator: MD shakib Hasan\n")
        f.write("# What's app: +8801610598422\n# Telegram: https://t.me/ibstvbd\n")
        f.write("# Our official partner : IBS TV. STAR SHARE. OPPLEX.\n\n")

        # সর্টিং (ক্যাটাগরি অনুযায়ী)
        all_channels.sort(key=lambda x: ORDERED_CATEGORIES.index(x['group']) if x['group'] in ORDERED_CATEGORIES else 99)

        for ch in all_channels:
            f.write(f'#EXTINF:-1 tvg-logo="{ch["logo"]}" group-title="{ch["group"]}",{ch["name"]}\n{ch["url"]}\n')

if __name__ == "__main__":
    final_channels = []
    for source_name, url in M3U_SOURCES.items():
        final_channels.extend(fetch_m3u(url))
    
    write_m3u(final_channels)
    
