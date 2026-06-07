import requests
import json
import datetime

# কনফিগারেশন
JSON_URLS = [
    "https://raw.githubusercontent.com/srhady/tapmad-bd/refs/heads/main/tapmad_bd.json",
    "https://raw.githubusercontent.com/srhady/toffee-bd/refs/heads/main/toffee_playlist.json",
    "https://raw.githubusercontent.com/srhady/bingstream/refs/heads/main/playlist.json",
    "https://raw.githubusercontent.com/srhady/data/refs/heads/main/playlist.json"
]
M3U_URL = "https://raw.githubusercontent.com/sm-monirulislam/AynaOTT-auto-update-playlist/refs/heads/main/AynaOTT.m3u"
FALLBACK_VIDEO = "https://raw.githubusercontent.com/ibstvofficial/IBS-TV-special-movies.m3u/refs/heads/main/1777291577865.mp4"
FALLBACK_LOGO = "https://camo.githubusercontent.com/93929647baabb50606ccf95056c8ff42b3f2f9249c5364fa1e0f8b7dcef395f3/68747470733a2f2f626469786970747662642e636f6d2f6c6f676f2e706e67"

def fetch_data():
    channels = []
    # FIFA Category যোগ করা
    for url in JSON_URLS:
        try:
            resp = requests.get(url).json()
            for item in resp:
                name = item.get("name", "").upper()
                if "BTV" in name or "SOMOY" in name:
                    item["group"] = "FIFA world cup 4k"
                channels.append(item)
        except: continue
    return channels

def write_m3u(channels):
    with open("FIFA-world-cup-4k.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write(f"# Playlist update dates and times: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# Playlist owner: STAR OTT BD\n# Playlist Creator: MD shakib Hasan\n")
        f.write("# What's app: +8801610598422\n# Telegram: https://t.me/ibstvbd\n")
        f.write("# Our official partner : IBS TV. STAR SHARE. OPPLEX.\n\n")

        # সর্টিং: FIFA সবার উপরে
        sorted_channels = sorted(channels, key=lambda x: x.get('group', 'ZZZ') != "FIFA world cup 4k")

        for ch in sorted_channels:
            url = ch.get("stream_url", FALLBACK_VIDEO)
            if not url: url = FALLBACK_VIDEO
            
            f.write(f"#EXTINF:-1 tvg-logo=\"{ch.get('logo', FALLBACK_LOGO)}\" group-title=\"{ch.get('group', 'General')}\",{ch.get('name')}\n")
            f.write(f"{url}\n")

channels = fetch_data()
write_m3u(channels)
