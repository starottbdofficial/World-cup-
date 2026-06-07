import requests
import datetime

JSON_URLS = [
    "https://raw.githubusercontent.com/srhady/tapmad-bd/refs/heads/main/tapmad_bd.json",
    "https://raw.githubusercontent.com/srhady/toffee-bd/refs/heads/main/toffee_playlist.json",
    "https://raw.githubusercontent.com/srhady/bingstream/refs/heads/main/playlist.json",
    "https://raw.githubusercontent.com/srhady/data/refs/heads/main/playlist.json"
]

FALLBACK_VIDEO = "https://raw.githubusercontent.com/ibstvofficial/IBS-TV-special-movies.m3u/refs/heads/main/1777291577865.mp4"
FALLBACK_LOGO = "https://camo.githubusercontent.com/93929647baabb50606ccf95056c8ff42b3f2f9249c5364fa1e0f8b7dcef395f3/68747470733a2f2f626469786970747662642e636f6d2f6c6f676f2e706e67"

def get_channels():
    all_channels = []
    for url in JSON_URLS:
        try:
            data = requests.get(url, timeout=10).json()
            for ch in data:
                name = ch.get("name", "")
                # ক্যাটাগরি সেট করা
                if "BTV" in name.upper() or "SOMOY" in name.upper():
                    ch["group"] = "FIFA world cup 4k"
                else:
                    ch["group"] = ch.get("group", "General")
                all_channels.append(ch)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    return all_channels

def create_m3u(channels):
    with open("FIFA-world-cup-4k.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write(f"# Playlist update dates and times: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# Playlist owner: STAR OTT BD\n# Playlist Creator: MD shakib Hasan\n")
        f.write("# What's app: +8801610598422\n# Telegram: https://t.me/ibstvbd\n")
        f.write("# Our official partner : IBS TV. STAR SHARE. OPPLEX.\n\n")

        # FIFA ক্যাটাগরি উপরে আনা
        channels.sort(key=lambda x: x.get('group') != "FIFA world cup 4k")

        for ch in channels:
            url = ch.get("stream_url") or FALLBACK_VIDEO
            logo = ch.get("logo") or FALLBACK_LOGO
            f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{ch.get("group")}",{ch.get("name")}\n')
            f.write(f"{url}\n")

if __name__ == "__main__":
    channels = get_channels()
    create_m3u(channels)
    
