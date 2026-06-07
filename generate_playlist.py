import requests
import datetime
import re

# সোর্স লিঙ্ক
M3U_SOURCES = {
    "Ayna": "https://raw.githubusercontent.com/sm-monirulislam/AynaOTT-auto-update-playlist/refs/heads/main/AynaOTT.m3u",
    "IPTVOrg": "https://iptv-org.github.io/iptv/index.m3u",
    "Akash": "https://raw.githubusercontent.com/srhady/Hady/refs/heads/main/akash_live.m3u"
}

# আপনার নির্ধারিত ক্যাটাগরি ম্যাপিং
CATEGORY_MAP = {
    "FIFA World cup": ["SOMOY", "BTV", "T SPORTS", "FIFA+"],
    "News": ["NEWS", "BBC", "CNN", "AL JAZEERA", "CHANNEL 24", "JOMUNA", "INDEPENDENT"],
    "Sports": ["SPORTS", "CRICKET", "FOOTBALL", "GOLF", "TEN", "ESPN"],
    "Bangladesh": ["BD", "BANGLA", "DHAKA", "CHANNEL I", "ATN"],
    "Music": ["MUSIC", "SONG", "GAAN", "MTV"],
    "Kids": ["KIDS", "CARTOON", "NICK", "DISNEY", "POGO", "CBEEBIES"],
    "Movie": ["MOVIE", "FILM", "HBO", "STAR MOVIES", "CINEMA"]
}

ORDERED_CATEGORIES = list(CATEGORY_MAP.keys())

def get_category(name, group):
    name_up = name.upper()
    group_up = (group or "").upper()
    
    # ম্যাপিং অনুযায়ী ক্যাটাগরি নির্ধারণ
    for cat, keywords in CATEGORY_MAP.items():
        if any(k in name_up for k in keywords) or any(k in group_up for k in keywords):
            return cat
    return None # যদি কোনো ক্যাটাগরির সাথে না মিলে তবে বাদ যাবে

def fetch_m3u(url):
    channels = []
    try:
        resp = requests.get(url, timeout=30).text
        for match in re.finditer(r'#EXTINF:-1 tvg-logo="(.*?)".*?group-title="(.*?)".*?,(.*?)\n(.*?)\n', resp):
            logo, group, name, url_link = match.groups()
            cat = get_category(name, group)
            if cat: # শুধুমাত্র আপনার নির্ধারিত ক্যাটাগরির চ্যানেলগুলো যুক্ত হবে
                channels.append({"name": name, "group": cat, "logo": logo, "url": url_link})
    except: pass
    return channels

def write_m3u(all_channels):
    with open("FIFA-world-cup-4k.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("# Playlist update dates and times: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        f.write("# Playlist owner: STAR OTT BD\n# Playlist Creator: MD shakib Hasan\n")
        f.write("# What's app: +8801610598422\n# Telegram: https://t.me/ibstvbd\n")
        f.write("# Our official partner : IBS TV. STAR SHARE. OPPLEX.\n\n")

        # সর্টিং
        all_channels.sort(key=lambda x: ORDERED_CATEGORIES.index(x['group']))

        for ch in all_channels:
            f.write(f'#EXTINF:-1 tvg-logo="{ch["logo"]}" group-title="{ch["group"]}",{ch["name"]}\n{ch["url"]}\n')

if __name__ == "__main__":
    final_channels = []
    for source_name, url in M3U_SOURCES.items():
        final_channels.extend(fetch_m3u(url))
    write_m3u(final_channels)
        
