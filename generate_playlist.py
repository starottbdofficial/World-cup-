import requests
import datetime

# আপনার দেওয়া JSON লিঙ্কগুলো (এগুলো যদি Matches স্ট্রাকচার ব্যবহার করে)
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
            
            # যদি JSON-এ 'Matches' কি (key) থাকে
            if "Matches" in data:
                items = data["Matches"]
            else:
                items = data # যদি সরাসরি লিস্ট হয়
            
            for item in items:
                name = item.get("VideoName", item.get("name", "Unknown Channel"))
                stream_url = item.get("stream_url", "")
                logo = item.get("ThumbnailStandard", item.get("logo", FALLBACK_LOGO))
                
                # ক্যাটাগরি লজিক
                group = item.get("CategoryName", item.get("group", "Others"))
                if "BTV" in name.upper() or "SOMOY" in name.upper():
                    group = "FIFA world cup 4k"
                
                all_channels.append({
                    "name": name,
                    "stream_url": stream_url,
                    "logo": logo,
                    "group": group
                })
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    return all_channels

def create_m3u(channels):
    with open("FIFA-world-cup-4k.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write(f"# Playlist update dates and times: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# Playlist owner: STAR OTT BD\n# Playlist Creator: MD shakib Hasan\n")
        f.write("# What's app: +8801610598422\n# Telegram: https://t.me/ibstvbdn")
        f.write("# Our official partner : IBS TV. STAR SHARE. OPPLEX.\n\n")

        # FIFA ক্যাটাগরি উপরে আনা
        channels.sort(key=lambda x: x['group'] != "FIFA world cup 4k")

        for ch in channels:
            url = ch["stream_url"] if ch["stream_url"] else FALLBACK_VIDEO
            f.write(f'#EXTINF:-1 tvg-logo="{ch["logo"]}" group-title="{ch["group"]}",{ch["name"]}\n')
            f.write(f"{url}\n")

if __name__ == "__main__":
    channels = get_channels()
    create_m3u(channels)
    
