import requests
import datetime
import re

# সোর্স লিঙ্ক
JSON_URLS = [
    "https://raw.githubusercontent.com/srhady/bingstream/refs/heads/main/playlist.json",
    "https://raw.githubusercontent.com/srhady/data/refs/heads/main/playlist.json"
]
M3U_URL = "https://raw.githubusercontent.com/sm-monirulislam/AynaOTT-auto-update-playlist/refs/heads/main/AynaOTT.m3u"
FALLBACK_VIDEO = "https://raw.githubusercontent.com/ibstvofficial/IBS-TV-special-movies.m3u/refs/heads/main/1777291577865.mp4"
FALLBACK_LOGO = "https://camo.githubusercontent.com/93929647baabb50606ccf95056c8ff42b3f2f9249c5364fa1e0f8b7dcef395f3/68747470733a2f2f626469786970747662642e636f6d2f6c6f676f2e706e67"

def categorize_channel(name, original_group):
    name_up = name.upper()
    # FIFA World Cup ক্যাটাগরি
    if any(x in name_up for x in ["SOMOY", "BTV", "T SPORTS"]):
        return "FIFA World cup"
    
    # অন্যান্য ক্যাটাগরি ম্যাপিং
    group_map = {
        "Sports": ["SPORTS", "CRICKET", "FOOTBALL"],
        "Bangladesh": ["BD", "BANGLA", "DHAKA"],
        "Kolkata": ["KOLKATA", "WB"],
        "India": ["INDIA", "HINDI", "STAR"],
        "Kids": ["KIDS", "CARTOON"],
        "Movie": ["MOVIE", "FILM"],
        "Music": ["MUSIC"]
    }
    
    for category, keywords in group_map.items():
        if any(k in name_up for k in keywords):
            return category
    return original_group if original_group else "Others"

def fetch_and_process():
    channels = []
    
    # JSON সোর্স প্রসেসিং
    for url in JSON_URLS:
        try:
            data = requests.get(url, timeout=10).json()
            items = data.get("channels", data.get("matches", []))
            for item in items:
                name = item.get("channel_name", item.get("Match Title", "Unknown"))
                stream_url = item.get("stream_url", item.get("Stream URL", FALLBACK_VIDEO))
                if isinstance(stream_url, list): stream_url = stream_url[0].get("play_url") if isinstance(stream_url[0], dict) else stream_url[0]
                
                channels.append({
                    "name": name,
                    "group": categorize_channel(name, item.get("Category", "")),
                    "logo": item.get("logo_url", item.get("Match Poster", FALLBACK_LOGO)),
                    "url": stream_url or FALLBACK_VIDEO
                })
        except: continue

    # M3U সোর্স প্রসেসিং
    try:
        m3u_text = requests.get(M3U_URL).text
        pattern = r'#EXTINF:-1 tvg-logo="(.*?)".*?group-title="(.*?)".*?,(.*?)\n(.*?)\n'
        matches = re.findall(pattern, m3u_text)
        for logo, group, name, url in matches:
            channels.append({
                "name": name,
                "group": categorize_channel(name, group),
                "logo": logo,
                "url": url
            })
    except: pass
    
    return channels

def write_m3u(channels):
    # অর্ডারিং লিস্ট
    order = ["FIFA World cup", "Sports", "Bangladesh", "Kolkata", "India", "Kids", "Movie", "Music"]
    
    with open("FIFA-world-cup-4k.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write(f"# Playlist update dates and times: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# Playlist owner: STAR OTT BD\n# Playlist Creator: MD shakib Hasan\n")
        f.write("# What's app: +8801610598422\n# Telegram: https://t.me/ibstvbdn")
        f.write("# Our official partner : IBS TV. STAR SHARE. OPPLEX.\n\n")

        # সর্টিং
        channels.sort(key=lambda x: order.index(x['group']) if x['group'] in order else 99)

        for ch in channels:
            f.write(f'#EXTINF:-1 tvg-logo="{ch["logo"]}" group-title="{ch["group"]}",{ch["name"]}\n')
            f.write(f"{ch['url']}\n")

if __name__ == "__main__":
    write_m3u(fetch_and_process())
            
