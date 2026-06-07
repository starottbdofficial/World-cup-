import requests
import datetime
import re

# সোর্স লিস্ট
JSON_URLS = [
    "https://raw.githubusercontent.com/srhady/toffee-bd/refs/heads/main/toffee_playlist.json",
    "https://raw.githubusercontent.com/srhady/bingstream/refs/heads/main/playlist.json",
    "https://raw.githubusercontent.com/srhady/data/refs/heads/main/playlist.json"
]
M3U_URL = "https://raw.githubusercontent.com/sm-monirulislam/AynaOTT-auto-update-playlist/refs/heads/main/AynaOTT.m3u"
FALLBACK_VIDEO = "https://raw.githubusercontent.com/ibstvofficial/IBS-TV-special-movies.m3u/refs/heads/main/1777291577865.mp4"
FALLBACK_LOGO = "https://camo.githubusercontent.com/93929647baabb50606ccf95056c8ff42b3f2f9249c5364fa1e0f8b7dcef395f3/68747470733a2f2f626469786970747662642e636f6d2f6c6f676f2e706e67"

def get_stream_url(data):
    # সব ধরণের স্ট্রিম ইউআরএল ফরম্যাট হ্যান্ডেল করার লজিক
    if isinstance(data, list):
        if len(data) > 0:
            item = data[0]
            return item.get("play_url") if isinstance(item, dict) else item
    elif isinstance(data, str):
        return data if data != "N/A" else None
    return None

def fetch_and_process():
    channels = []
    
    # JSON সোর্স থেকে প্রসেস করা
    for url in JSON_URLS:
        try:
            data = requests.get(url, timeout=10).json()
            # বিভিন্ন কী (key) থেকে চ্যানেল লিস্ট খুঁজে বের করা
            items = data.get("channels", data.get("matches", data))
            if not isinstance(items, list): items = [items]
            
            for item in items:
                name = item.get("channel_name", item.get("Match Title", "Unknown Channel"))
                group = item.get("Category", item.get("category", "General"))
                # FIFA ক্যাটাগরি লজিক
                if "BTV" in name.upper() or "SOMOY" in name.upper(): group = "FIFA world cup 4k"
                
                channels.append({
                    "name": name,
                    "group": group,
                    "logo": item.get("logo_url", item.get("Match Poster", FALLBACK_LOGO)),
                    "url": get_stream_url(item.get("Stream URL", item.get("stream_url"))) or FALLBACK_VIDEO
                })
        except: continue

    # M3U সোর্স থেকে প্রসেস করা
    try:
        m3u_data = requests.get(M3U_URL).text
        for line in m3u_data.splitlines():
            if line.startswith("#EXTINF"):
                # M3U থেকে নাম ও লোগো এক্সট্রাক্ট করা (Regex)
                name = line.split(",")[-1]
                channels.append({"name": name, "group": "AynaOTT", "logo": FALLBACK_LOGO, "url": FALLBACK_VIDEO})
    except: pass
    
    return channels

def write_m3u(channels):
    with open("FIFA-world-cup-4k.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write(f"# Playlist update dates and times: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# Playlist owner: STAR OTT BD\n# Playlist Creator: MD shakib Hasan\n")
        f.write("# What's app: +8801610598422\n# Telegram: https://t.me/ibstvbdn")
        f.write("# Our official partner : IBS TV. STAR SHARE. OPPLEX.\n\n")

        # সর্টিং: FIFA সবার উপরে
        channels.sort(key=lambda x: x['group'] != "FIFA world cup 4k")

        for ch in channels:
            f.write(f'#EXTINF:-1 tvg-logo="{ch["logo"]}" group-title="{ch["group"]}",{ch["name"]}\n')
            f.write(f"{ch['url']}\n")

if __name__ == "__main__":
    data = fetch_and_process()
    write_m3u(data)
        
